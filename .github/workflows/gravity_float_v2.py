"""
Module: gravity_float_v2.py
Description: Gravity-Float Core v2 - Dynamic Ephemeris & Relative Orbital Energy Analysis.
             基于 JPL 公開參數，所有天體動態傳播，嚴格區分 Flyby 與 Bound Capture。
Author: Engineering Assistant
License: MIT
SIMULATION ONLY - 無實體控制介面
"""

import numpy as np
from scipy.integrate import solve_ivp
from dataclasses import dataclass
from typing import List, Dict, Tuple

# ============================================================================
# 01 & 02: DATA GATEWAY & CELESTIAL STATE (NASA/JPL 常數)
# ============================================================================
AU = 1.495978707e8          # km
DAY_SEC = 86400.0
MU_SUN = 1.32712440018e11   # km^3/s^2
MU_EARTH = 3.986004418e5
MU_MARS = 4.282837e4
MU_PSYCHE = 1.601           # 2024 最新高精度值 (Farnocchia et al.)

@dataclass
class Body:
    name: str
    mu: float                # GM (km^3/s^2)
    pos: np.ndarray          # 日心位置 (km)
    vel: np.ndarray          # 日心速度 (km/s)

class KeplerPropagator:
    """簡化二體軌道傳播 (僅用於背景行星，不包含相互攝動)"""
    @staticmethod
    def circular_velocity(radius: float, mu: float) -> float:
        return np.sqrt(mu / radius)

    @staticmethod
    def propagate_earth(t_sec: float) -> Body:
        """地球：近似圓軌道，角速度 n = sqrt(mu/a^3)"""
        a = 1.0 * AU
        n = np.sqrt(MU_SUN / a**3)
        theta = n * t_sec
        pos = np.array([a * np.cos(theta), a * np.sin(theta), 0])
        vel = np.array([-a * n * np.sin(theta), a * n * np.cos(theta), 0])
        return Body("Earth", MU_EARTH, pos, vel)

    @staticmethod
    def propagate_mars(t_sec: float) -> Body:
        """火星：近似圓軌道"""
        a = 1.5237 * AU
        n = np.sqrt(MU_SUN / a**3)
        theta = n * t_sec + 0.8  # 相位偏移
        pos = np.array([a * np.cos(theta), a * np.sin(theta), 0])
        vel = np.array([-a * n * np.sin(theta), a * n * np.cos(theta), 0])
        return Body("Mars", MU_MARS, pos, vel)

    @staticmethod
    def propagate_psyche(t_sec: float) -> Body:
        """
        16 Psyche：橢圓軌道 (克卜勒方程數值解)
        根數 (近似值，對應 2029 窗口):
        a = 2.9235 AU, e = 0.1343, i = 3.1°, Ω=150°, ω=229.75°
        """
        a = 2.9235 * AU
        e = 0.1343
        i = np.radians(3.1)
        Omega = np.radians(150.01)
        w = np.radians(229.75)
        
        # 初始近點角 (設定 t=0 時約在近日點後某處)
        M0 = np.radians(40.64)  
        n = np.sqrt(MU_SUN / a**3)
        M = M0 + n * t_sec
        
        # 解克卜勒方程 E - e*sin(E) = M
        E = M
        for _ in range(10):
            E = E - (E - e*np.sin(E) - M) / (1 - e*np.cos(E))
        
        # 真近點角
        nu = 2 * np.arctan2(np.sqrt(1+e) * np.sin(E/2), np.sqrt(1-e) * np.cos(E/2))
        r = a * (1 - e*np.cos(E))
        
        # 軌道面內位置 (x' 指向近日點)
        x_orb = r * np.cos(nu)
        y_orb = r * np.sin(nu)
        
        # 軌道面內速度
        p = a * (1 - e**2)
        vx_orb = -np.sqrt(MU_SUN / p) * np.sin(nu)
        vy_orb = np.sqrt(MU_SUN / p) * (e + np.cos(nu))
        
        # 旋轉至日心黃道座標 (R3(-Omega) * R1(-i) * R3(-w))
        cosO, sinO = np.cos(Omega), np.sin(Omega)
        cosi, sini = np.cos(i), np.sin(i)
        cosw, sinw = np.cos(w), np.sin(w)
        
        # 位置旋轉
        x = (cosO*cosw - sinO*sinw*cosi)*x_orb + (-cosO*sinw - sinO*cosw*cosi)*y_orb
        y = (sinO*cosw + cosO*sinw*cosi)*x_orb + (-sinO*sinw + cosO*cosw*cosi)*y_orb
        z = (sinw*sini)*x_orb + (cosw*sini)*y_orb
        
        # 速度旋轉 (同矩陣)
        vx = (cosO*cosw - sinO*sinw*cosi)*vx_orb + (-cosO*sinw - sinO*cosw*cosi)*vy_orb
        vy = (sinO*cosw + cosO*sinw*cosi)*vx_orb + (-sinO*sinw + cosO*cosw*cosi)*vy_orb
        vz = (sinw*sini)*vx_orb + (cosw*sini)*vy_orb
        
        return Body("16 Psyche", MU_PSYCHE, np.array([x, y, z]), np.array([vx, vy, vz]))

# ============================================================================
# 03 & 04: GRAVITY CORE & N-BODY INTEGRATOR
# ============================================================================
class GravityCore:
    @staticmethod
    def acceleration(pos_sc: np.ndarray, bodies: List[Body]) -> np.ndarray:
        """計算所有天體對探測器的重力加速度 (km/s^2)"""
        acc = np.zeros(3)
        for body in bodies:
            delta = body.pos - pos_sc
            dist_sq = np.dot(delta, delta)
            if dist_sq < 1e-12:
                continue
            dist = np.sqrt(dist_sq)
            acc += body.mu * delta / (dist_sq * dist)
        return acc

class NBodyEngine:
    def __init__(self, sc_initial_pos: np.ndarray, sc_initial_vel: np.ndarray):
        self.sc_pos = sc_initial_pos
        self.sc_vel = sc_initial_vel

    def _derivatives(self, t: float, state: np.ndarray) -> np.ndarray:
        pos = state[0:3]
        vel = state[3:6]
        
        # 即時取得所有天體當前位置 (動態星曆)
        bodies = [
            KeplerPropagator.propagate_earth(t),
            KeplerPropagator.propagate_mars(t),
            KeplerPropagator.propagate_psyche(t),
            # 太陽固定於質心，但數值上可忽略其對探測器的微小影響，或加入固定 Body
            Body("Sun", MU_SUN, np.array([0,0,0]), np.array([0,0,0]))
        ]
        
        acc = GravityCore.acceleration(pos, bodies)
        return np.concatenate([vel, acc])

    def simulate(self, duration_days: float, step_min: float = 1.0) -> Dict:
        t_span = (0, duration_days * DAY_SEC)
        t_eval = np.linspace(0, duration_days * DAY_SEC, int(duration_days * DAY_SEC / (step_min * 60)))
        state0 = np.concatenate([self.sc_pos, self.sc_vel])
        
        sol = solve_ivp(self._derivatives, t_span, state0, t_eval=t_eval, method='RK45', rtol=1e-10, atol=1e-12)
        if not sol.success:
            raise RuntimeError(f"Integration failed: {sol.message}")
        
        return {
            "t_days": sol.t / DAY_SEC,
            "pos_sc": sol.y[0:3].T,
            "vel_sc": sol.y[3:6].T,
        }

# ============================================================================
# 05 & 06: RELATIVE-STATE ENGINE & GRAVITY-FLOAT ANALYZER (能量判據)
# ============================================================================
class RelativeStateAnalyzer:
    @staticmethod
    def analyze(t_days: np.ndarray, pos_sc: np.ndarray, vel_sc: np.ndarray) -> List[Dict]:
        """
        逐點計算相對於 Psyche 的狀態，並計算比軌道能量。
        """
        results = []
        for i in range(len(t_days)):
            # 計算該時刻 Psyche 的真實狀態 (必須重新傳播以對齊時間)
            psyche = KeplerPropagator.propagate_psyche(t_days[i] * DAY_SEC)
            
            r_rel = pos_sc[i] - psyche.pos
            v_rel = vel_sc[i] - psyche.vel
            dist = np.linalg.norm(r_rel)
            
            # 避免除以零
            if dist < 1.0:
                dist = 1.0
            
            # 比軌道能量 (Specific Orbital Energy) ε = v^2/2 - μ/r
            v_rel_mag = np.linalg.norm(v_rel)
            epsilon = (v_rel_mag**2 / 2) - (MU_PSYCHE / dist)
            
            # 狀態分類
            if epsilon < 0:
                status = "BOUND (重力捕獲)" if dist < 5000 else "BOUND (遠距束縛)"
            else:
                # 檢查是否正在接近 (徑向速度 < 0)
                r_hat = r_rel / dist
                v_r = np.dot(v_rel, r_hat)
                if v_r < 0:
                    status = "FLYBY (接近中)"
                else:
                    status = "FLYBY (遠離中)"
            
            results.append({
                "time_days": t_days[i],
                "distance_km": dist,
                "rel_speed_km_s": v_rel_mag,
                "specific_energy_km2_s2": epsilon,
                "status": status
            })
        return results

# ============================================================================
# 07 & 08: VALIDATION & SAFETY
# ============================================================================
SIMULATION_ONLY = True
if not SIMULATION_ONLY:
    raise RuntimeError("Safety block: Real-world deployment disabled.")

# ============================================================================
# MAIN EXECUTION (模擬 2029 接近窗口)
# ============================================================================
if __name__ == "__main__":
    print("="*70)
    print("        GRAVITY-FLOAT v2 — 動態星曆與軌道能量分析")
    print("="*70)
    print("⚠️  純數值模擬 | 無實體控制指令 | 基於 JPL 公開參數\n")

    # 初始狀態設定：假設探測器在 2029 年 7 月前某時刻，距離 Psyche 約 10 萬公里，相對速度極低 (模擬接近)
    # 先取得 t=0 時的 Psyche 狀態作為初始條件基準
    psyche_init = KeplerPropagator.propagate_psyche(0)
    sc_init_pos = psyche_init.pos + np.array([100000.0, 0.0, 0.0])   # 相距 10 萬公里
    sc_init_vel = psyche_init.vel + np.array([-0.05, 0.02, 0.0])     # 相對速度約 0.054 km/s (緩慢接近)

    engine = NBodyEngine(sc_init_pos, sc_init_vel)
    
    # 模擬 30 天 (觀察捕獲或飛掠過程)
    print("[INFO] 啟動 N-body 積分 (模擬 30 天, 時間步長 1 分鐘)...")
    raw_results = engine.simulate(duration_days=30.0, step_min=1.0)
    
    # 進行相對狀態與能量分析
    analyzer = RelativeStateAnalyzer()
    analysis = analyzer.analyze(raw_results["t_days"], raw_results["pos_sc"], raw_results["vel_sc"])
    
    # 輸出關鍵時刻 (初始、最接近、最終)
    print("\n" + "="*70)
    print("                   分析報告 (取關鍵幀)")
    print("="*70)
    
    # 找出最接近 Psyche 的點 (最小距離)
    min_dist_idx = np.argmin([d["distance_km"] for d in analysis])
    closest = analysis[min_dist_idx]
    
    print(f"\n[初始狀態] 時間: {analysis[0]['time_days']:.2f} 天")
    print(f"  距離: {analysis[0]['distance_km']:,.0f} km | 相對速度: {analysis[0]['rel_speed_km_s']:.4f} km/s")
    print(f"  比能量: {analysis[0]['specific_energy_km2_s2']:.4f} km²/s² | 狀態: {analysis[0]['status']}")
    
    print(f"\n[最接近點] 時間: {closest['time_days']:.2f} 天")
    print(f"  距離: {closest['distance_km']:,.0f} km | 相對速度: {closest['rel_speed_km_s']:.4f} km/s")
    print(f"  比能量: {closest['specific_energy_km2_s2']:.6f} km²/s² | 狀態: {closest['status']}")
    
    print(f"\n[最終狀態] 時間: {analysis[-1]['time_days']:.2f} 天")
    print(f"  距離: {analysis[-1]['distance_km']:,.0f} km | 相對速度: {analysis[-1]['rel_speed_km_s']:.4f} km/s")
    print(f"  比能量: {analysis[-1]['specific_energy_km2_s2']:.4f} km²/s² | 狀態: {analysis[-1]['status']}")
    
    # 科學結論
    if closest['specific_energy_km2_s2'] < 0 and closest['distance_km'] < 10000:
        print("\n[科學結論] ✅ 探測器在接近點具備負能量，符合『重力捕獲』的力學條件 (視後續軌道穩定與否)。")
    else:
        print("\n[科學結論] ⚠️  探測器能量為正，僅為『重力飛掠 (Flyby)』，無法自然被 Psyche 捕獲。")
    
    print("\n[驗證] 所有天體位置隨時間動態更新，相對速度基於 v_sc - v_psyche 計算。")
    print("[安全] SIMULATION_ONLY 旗標已啟用。")
