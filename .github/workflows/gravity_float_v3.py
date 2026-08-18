"""
Module: gravity_float_v3.py
Description: Gravity-Float Core v3 - Dual Mode (REAL / HYPER) with Orbit Diagnostics.
             嚴格拆分: Psyche 星曆使用真實 μ；探測器受力使用可切換有效 μ。
             診斷: 結合 ε、徑向速度、近心點、束縛持續時間。
Author: Engineering Assistant
License: MIT
SIMULATION ONLY — 無實體控制介面
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

# 16 Psyche 真實引力參數 (用於星曆傳播)
MU_PSYCHE_REAL = 1.601      # Farnocchia et al. 2024

# ============================================================================
# 可切換實驗參數 (僅影響探測器受力，不影響 Psyche 軌道)
# ============================================================================
# 用戶可修改此處：
HYPER_MULTIPLIER = 1000.0    # 設為 1.0 即為真實模式 (REAL)
MU_PSYCHE_EFFECTIVE = MU_PSYCHE_REAL * HYPER_MULTIPLIER

# 診斷閾值
BOUND_DIST_THRESHOLD = 5000  # km (用於標示「近距離束縛」)

@dataclass
class Body:
    name: str
    mu: float                # GM (km^3/s^2)
    pos: np.ndarray          # 日心位置 (km)
    vel: np.ndarray          # 日心速度 (km/s)

class KeplerPropagator:
    """使用真實 μ 傳播星曆 (不隨 HYPER 模式變動)"""
    @staticmethod
    def propagate_earth(t_sec: float) -> Body:
        a = 1.0 * AU
        n = np.sqrt(MU_SUN / a**3)
        theta = n * t_sec
        pos = np.array([a * np.cos(theta), a * np.sin(theta), 0.0])
        vel = np.array([-a * n * np.sin(theta), a * n * np.cos(theta), 0.0])
        return Body("Earth", MU_EARTH, pos, vel)

    @staticmethod
    def propagate_mars(t_sec: float) -> Body:
        a = 1.5237 * AU
        n = np.sqrt(MU_SUN / a**3)
        theta = n * t_sec + 0.8
        pos = np.array([a * np.cos(theta), a * np.sin(theta), 0.0])
        vel = np.array([-a * n * np.sin(theta), a * n * np.cos(theta), 0.0])
        return Body("Mars", MU_MARS, pos, vel)

    @staticmethod
    def propagate_psyche(t_sec: float) -> Body:
        """
        Psyche 星曆: 僅使用 MU_PSYCHE_REAL 計算軌道。
        此函數不受 HYPER_MULTIPLIER 影響。
        """
        a = 2.9235 * AU
        e = 0.1343
        i = np.radians(3.1)
        Omega = np.radians(150.01)
        w = np.radians(229.75)
        M0 = np.radians(40.64)
        n = np.sqrt(MU_SUN / a**3)
        M = M0 + n * t_sec

        # 解克卜勒方程
        E = M
        for _ in range(12):
            E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))

        nu = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2),
                           np.sqrt(1 - e) * np.cos(E / 2))
        r = a * (1 - e * np.cos(E))
        x_orb = r * np.cos(nu)
        y_orb = r * np.sin(nu)

        p = a * (1 - e**2)
        vx_orb = -np.sqrt(MU_SUN / p) * np.sin(nu)
        vy_orb = np.sqrt(MU_SUN / p) * (e + np.cos(nu))

        cosO, sinO = np.cos(Omega), np.sin(Omega)
        cosi, sini = np.cos(i), np.sin(i)
        cosw, sinw = np.cos(w), np.sin(w)

        # 位置旋轉
        x = (cosO*cosw - sinO*sinw*cosi)*x_orb + (-cosO*sinw - sinO*cosw*cosi)*y_orb
        y = (sinO*cosw + cosO*sinw*cosi)*x_orb + (-sinO*sinw + cosO*cosw*cosi)*y_orb
        z = (sinw*sini)*x_orb + (cosw*sini)*y_orb

        # 速度旋轉
        vx = (cosO*cosw - sinO*sinw*cosi)*vx_orb + (-cosO*sinw - sinO*cosw*cosi)*vy_orb
        vy = (sinO*cosw + cosO*sinw*cosi)*vx_orb + (-sinO*sinw + cosO*cosw*cosi)*vy_orb
        vz = (sinw*sini)*vx_orb + (cosw*sini)*vy_orb

        # 注意: 此處 Body.mu 仍設為真實值，僅供參考；實際受力由 NBodyEngine 覆寫。
        return Body("16 Psyche", MU_PSYCHE_REAL, np.array([x, y, z]), np.array([vx, vy, vz]))

# ============================================================================
# 03 & 04: GRAVITY CORE & N-BODY INTEGRATOR (支援有效 μ 切換)
# ============================================================================
class GravityCore:
    @staticmethod
    def acceleration(pos_sc: np.ndarray, bodies: List[Body], effective_mu_psyche: float) -> np.ndarray:
        """
        計算加速度。
        - 太陽、地球、火星：使用自身真實 μ。
        - Psyche：使用傳入的 effective_mu_psyche (可為真實值或放大值)。
        """
        acc = np.zeros(3)
        for body in bodies:
            # 決定該天體使用的 μ
            if body.name == "16 Psyche":
                mu = effective_mu_psyche
            else:
                mu = body.mu
            
            delta = body.pos - pos_sc
            dist_sq = np.dot(delta, delta)
            if dist_sq < 1e-12:
                continue
            dist = np.sqrt(dist_sq)
            acc += mu * delta / (dist_sq * dist)
        return acc

class NBodyEngine:
    def __init__(self, sc_initial_pos: np.ndarray, sc_initial_vel: np.ndarray,
                 effective_mu_psyche: float):
        self.sc_pos = sc_initial_pos
        self.sc_vel = sc_initial_vel
        self.effective_mu_psyche = effective_mu_psyche

    def _derivatives(self, t: float, state: np.ndarray) -> np.ndarray:
        pos = state[0:3]
        vel = state[3:6]
        
        # 取得當前星曆 (所有天體位置)
        bodies = [
            KeplerPropagator.propagate_earth(t),
            KeplerPropagator.propagate_mars(t),
            KeplerPropagator.propagate_psyche(t),
            Body("Sun", MU_SUN, np.zeros(3), np.zeros(3))
        ]
        
        # 計算加速度時，傳入 effective_mu_psyche
        acc = GravityCore.acceleration(pos, bodies, self.effective_mu_psyche)
        return np.concatenate([vel, acc])

    def simulate(self, duration_days: float, step_min: float = 1.0) -> Dict:
        t_span = (0.0, duration_days * DAY_SEC)
        t_eval = np.linspace(0.0, duration_days * DAY_SEC,
                             int(duration_days * DAY_SEC / (step_min * 60)) + 1)
        state0 = np.concatenate([self.sc_pos, self.sc_vel])
        sol = solve_ivp(self._derivatives, t_span, state0, t_eval=t_eval,
                        method='RK45', rtol=1e-10, atol=1e-12)
        if not sol.success:
            raise RuntimeError(f"Integration failed: {sol.message}")
        return {
            "t_days": sol.t / DAY_SEC,
            "pos_sc": sol.y[0:3].T,
            "vel_sc": sol.y[3:6].T,
        }

# ============================================================================
# 05 & 06: RELATIVE-STATE ENGINE & ORBIT DIAGNOSTICS (v3 核心升級)
# ============================================================================
class OrbitDiagnostics:
    @staticmethod
    def analyze(t_days: np.ndarray, pos_sc: np.ndarray, vel_sc: np.ndarray,
                effective_mu: float) -> Dict:
        """
        綜合診斷: 不僅看瞬時 ε，更追蹤徑向速度、近心點、束縛持續時間。
        """
        results = []
        bound_counter = 0
        max_bound_duration = 0.0
        periapsis_detected = False
        min_dist = 1e12
        min_dist_idx = 0
        epsilon_at_periapsis = 0.0

        for i in range(len(t_days)):
            psyche = KeplerPropagator.propagate_psyche(t_days[i] * DAY_SEC)
            r_rel = pos_sc[i] - psyche.pos
            v_rel = vel_sc[i] - psyche.vel
            dist = np.linalg.norm(r_rel)
            if dist < 1.0:
                dist = 1.0
            
            v_rel_mag = np.linalg.norm(v_rel)
            # 比軌道能量 (使用 effective_mu)
            epsilon = (v_rel_mag**2 / 2.0) - (effective_mu / dist)
            
            # 徑向速度 (負值代表接近)
            r_hat = r_rel / dist
            v_r = np.dot(v_rel, r_hat)
            
            # 追蹤最小距離 (近心點)
            if dist < min_dist:
                min_dist = dist
                min_dist_idx = i
                epsilon_at_periapsis = epsilon
                # 檢查是否在近心點處速度方向轉折 (v_r 由負轉正)
                if i > 0:
                    prev_vr = results[-1]["radial_velocity_km_s"]
                    if prev_vr < 0 and v_r >= 0:
                        periapsis_detected = True

            # 束縛持續時間 (ε < 0 的連續計數)
            if epsilon < 0:
                bound_counter += 1
            else:
                bound_counter = 0
            max_bound_duration = max(max_bound_duration, bound_counter * (t_days[1] - t_days[0]))

            # 狀態分類 (多條件)
            if epsilon < 0 and dist < BOUND_DIST_THRESHOLD:
                status = "BOUND (近距離束縛)"
            elif epsilon < 0:
                status = "BOUND (遠距弱束縛)"
            else:
                if v_r < 0:
                    status = "FLYBY (接近中)"
                else:
                    status = "FLYBY (遠離中)"

            results.append({
                "time_days": t_days[i],
                "distance_km": dist,
                "rel_speed_km_s": v_rel_mag,
                "specific_energy_km2_s2": epsilon,
                "radial_velocity_km_s": v_r,
                "status": status
            })

        # 最終判定
        final_status = results[-1]["status"]
        final_dist = results[-1]["distance_km"]
        is_bound_overall = (max_bound_duration > 0.5 and 
                            results[min_dist_idx]["specific_energy_km2_s2"] < 0)

        return {
            "timeline": results,
            "min_dist_km": min_dist,
            "min_dist_time_days": t_days[min_dist_idx],
            "epsilon_at_periapsis": epsilon_at_periapsis,
            "periapsis_detected": periapsis_detected,
            "max_bound_duration_days": max_bound_duration,
            "final_distance_km": final_dist,
            "final_status": final_status,
            "is_captured": is_bound_overall and periapsis_detected and final_dist < 20000
        }

# ============================================================================
# 07 & 08: VALIDATION & SAFETY
# ============================================================================
SIMULATION_ONLY = True
if not SIMULATION_ONLY:
    raise RuntimeError("Safety block: Real-world deployment disabled.")

# ============================================================================
# MAIN EXECUTION
# ============================================================================
if __name__ == "__main__":
    # 顯示當前模式
    mode_name = "REAL (真實引力)" if HYPER_MULTIPLIER == 1.0 else f"HYPER (放大 {HYPER_MULTIPLIER:.0f}×)"
    
    print("=" * 70)
    print(f"   GRAVITY-FLOAT v3 — 雙模式軌道診斷器")
    print("=" * 70)
    print(f"當前模式  : {mode_name}")
    print(f"星曆 μ    : {MU_PSYCHE_REAL:.3f} km³/s² (固定真實值)")
    print(f"受力有效 μ: {MU_PSYCHE_EFFECTIVE:.3f} km³/s² (僅影響探測器)")
    print("⚠️  純模擬 | 無實體控制 | 診斷包含 ε, 徑向速度, 近心點, 束縛持續時間\n")

    # 初始條件 (t=0 時，探測器距 Psyche 10 萬公里，相對速度極低)
    psyche_init = KeplerPropagator.propagate_psyche(0.0)
    sc_init_pos = psyche_init.pos + np.array([100000.0, 0.0, 0.0])
    sc_init_vel = psyche_init.vel + np.array([-0.05, 0.02, 0.0])

    engine = NBodyEngine(sc_init_pos, sc_init_vel, MU_PSYCHE_EFFECTIVE)
    print("[INFO] 啟動 N-body 積分 (模擬 30 天)...")
    raw = engine.simulate(duration_days=30.0, step_min=1.0)

    # 執行診斷
    diag = OrbitDiagnostics.analyze(raw["t_days"], raw["pos_sc"], raw["vel_sc"], MU_PSYCHE_EFFECTIVE)

    print("\n" + "=" * 70)
    print("                   軌道診斷報告 (v3)")
    print("=" * 70)
    print(f"最接近距離        : {diag['min_dist_km']:,.0f} km (發生於第 {diag['min_dist_time_days']:.2f} 天)")
    print(f"近心點能量 ε     : {diag['epsilon_at_periapsis']:.6f} km²/s²")
    print(f"近心點偵測 (v_r轉向): {'✅ 是' if diag['periapsis_detected'] else '❌ 否'}")
    print(f"最長連續束縛天數  : {diag['max_bound_duration_days']:.2f} 天")
    print(f"最終距離          : {diag['final_distance_km']:,.0f} km")
    print(f"最終狀態          : {diag['final_status']}")

    # 綜合分類
    if diag["is_captured"]:
        print("\n[科學結論] ✅ 綜合判據 (ε<0 + 近心點 + 持續束縛 + 最終未逃逸) → 判定為『重力捕獲』。")
    elif diag["max_bound_duration_days"] > 0.5:
        print("\n[科學結論] ⚠️  曾短暫進入負能狀態，但未滿足完整捕獲條件 (可能為『臨時束縛』或『近距離飛掠』)。")
    else:
        print("\n[科學結論] ❌ 未形成穩定束縛，判別為『純飛掠 (Flyby)』。")

    print("\n[驗證] 星曆與受力 μ 已拆分；診斷結合多物理量，非僅依賴單一 ε 值。")
    print("[安全] SIMULATION_ONLY = True。")
