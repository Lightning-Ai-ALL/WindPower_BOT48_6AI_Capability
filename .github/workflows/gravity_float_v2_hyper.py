"""
Module: gravity_float_v2_hyper.py
Description: Gravity-Float Core v2 (Hypothetical 1000× Gravity Mode)
             動態星曆 + 相對軌道能量分析。引力強化僅為數值實驗。
Author: Engineering Assistant
License: MIT
SIMULATION ONLY — 無實體控制介面
"""

import numpy as np
from scipy.integrate import solve_ivp
from dataclasses import dataclass
from typing import List, Dict

# ============================================================================
# 01 & 02: DATA GATEWAY & CELESTIAL STATE
# ============================================================================
AU = 1.495978707e8          # km
DAY_SEC = 86400.0
MU_SUN = 1.32712440018e11   # km^3/s^2
MU_EARTH = 3.986004418e5
MU_MARS = 4.282837e4

# 真實值
MU_PSYCHE_REAL = 1.601      # Farnocchia et al. 2024

# 假設強化倍率（純數值實驗）
HYPER_GRAVITY_MULTIPLIER = 1000.0
MU_PSYCHE = MU_PSYCHE_REAL * HYPER_GRAVITY_MULTIPLIER

@dataclass
class Body:
    name: str
    mu: float
    pos: np.ndarray
    vel: np.ndarray

class KeplerPropagator:
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
        a = 2.9235 * AU
        e = 0.1343
        i = np.radians(3.1)
        Omega = np.radians(150.01)
        w = np.radians(229.75)
        M0 = np.radians(40.64)
        n = np.sqrt(MU_SUN / a**3)
        M = M0 + n * t_sec

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

        x = (cosO*cosw - sinO*sinw*cosi)*x_orb + (-cosO*sinw - sinO*cosw*cosi)*y_orb
        y = (sinO*cosw + cosO*sinw*cosi)*x_orb + (-sinO*sinw + cosO*cosw*cosi)*y_orb
        z = (sinw*sini)*x_orb + (cosw*sini)*y_orb

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
        bodies = [
            KeplerPropagator.propagate_earth(t),
            KeplerPropagator.propagate_mars(t),
            KeplerPropagator.propagate_psyche(t),
            Body("Sun", MU_SUN, np.zeros(3), np.zeros(3))
        ]
        acc = GravityCore.acceleration(pos, bodies)
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
# 05 & 06: RELATIVE-STATE ENGINE & ENERGY ANALYZER
# ============================================================================
class RelativeStateAnalyzer:
    @staticmethod
    def analyze(t_days: np.ndarray, pos_sc: np.ndarray, vel_sc: np.ndarray) -> List[Dict]:
        results = []
        for i in range(len(t_days)):
            psyche = KeplerPropagator.propagate_psyche(t_days[i] * DAY_SEC)
            r_rel = pos_sc[i] - psyche.pos
            v_rel = vel_sc[i] - psyche.vel
            dist = np.linalg.norm(r_rel)
            if dist < 1.0:
                dist = 1.0
            v_rel_mag = np.linalg.norm(v_rel)
            epsilon = (v_rel_mag**2 / 2.0) - (MU_PSYCHE / dist)

            if epsilon < 0.0:
                status = "BOUND (重力捕獲)" if dist < 5000 else "BOUND (遠距束縛)"
            else:
                r_hat = r_rel / dist
                v_r = np.dot(v_rel, r_hat)
                status = "FLYBY (接近中)" if v_r < 0 else "FLYBY (遠離中)"

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
# MAIN EXECUTION
# ============================================================================
if __name__ == "__main__":
    print("=" * 70)
    print("   GRAVITY-FLOAT v2 — 假設千倍引力模式 (純數值實驗)")
    print("=" * 70)
    print(f"真實 μ_Psyche = {MU_PSYCHE_REAL:.3f} km³/s²")
    print(f"實驗倍率     = {HYPER_GRAVITY_MULTIPLIER:.0f}×")
    print(f"實驗 μ_Psyche = {MU_PSYCHE:.1f} km³/s²")
    print("⚠️  純模擬 | 無實體控制 | 僅用於能量判據驗證\n")

    psyche_init = KeplerPropagator.propagate_psyche(0.0)
    # 初始相對距離 100 000 km，相對速度約 0.054 km/s
    sc_init_pos = psyche_init.pos + np.array([100000.0, 0.0, 0.0])
    sc_init_vel = psyche_init.vel + np.array([-0.05, 0.02, 0.0])

    engine = NBodyEngine(sc_init_pos, sc_init_vel)
    print("[INFO] 啟動 N-body 積分 (30 天)...")
    raw = engine.simulate(duration_days=30.0, step_min=1.0)

    analysis = RelativeStateAnalyzer.analyze(raw["t_days"], raw["pos_sc"], raw["vel_sc"])
    min_idx = np.argmin([d["distance_km"] for d in analysis])
    closest = analysis[min_idx]

    print("\n" + "=" * 70)
    print("                   分析報告 (關鍵幀)")
    print("=" * 70)
    print(f"\n[初始] 距離 {analysis[0]['distance_km']:,.0f} km | "
          f"ε = {analysis[0]['specific_energy_km2_s2']:.6f} | {analysis[0]['status']}")
    print(f"[最接近] 時間 {closest['time_days']:.2f} 天 | "
          f"距離 {closest['distance_km']:,.0f} km | "
          f"ε = {closest['specific_energy_km2_s2']:.6f} | {closest['status']}")
    print(f"[最終] 距離 {analysis[-1]['distance_km']:,.0f} km | "
          f"ε = {analysis[-1]['specific_energy_km2_s2']:.6f} | {analysis[-1]['status']}")

    if closest["specific_energy_km2_s2"] < 0 and closest["distance_km"] < 10000:
        print("\n[科學結論] 在千倍引力假設下，接近點具備負能量，符合束縛條件。")
    else:
        print("\n[科學結論] 即使強化千倍，在此初始條件下仍可能僅為飛掠。")

    print("\n[驗證] 所有天體動態傳播；相對速度 = v_sc − v_Psyche；")
    print("       捕獲判據嚴格採用比軌道能量 ε < 0。")
    print("[安全] SIMULATION_ONLY = True。")
