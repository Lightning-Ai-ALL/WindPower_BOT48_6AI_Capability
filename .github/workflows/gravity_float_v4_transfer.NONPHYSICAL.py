"""
Module: gravity_float_v4_transfer.NONPHYSICAL.py
Description: Gravity-Float Core v4 - Local Escape → Heliocentric Transfer → 1 AU Crossing.
             NON-PHYSICAL EXTREME NUMERICAL EXPERIMENT.
             修正 v4 缺陷：
             1. 初始相對速度設為 7.23 km/s（10,000× μ 逃逸速度）
             2. SOI_RADIUS → EXPERIMENTAL_SWITCH_RADIUS
             3. Mars 改為固定位置（非真實星曆）
             4. 捕獲判據改為 INSTANTANEOUS_BOUND（非永久捕獲）
Author: Engineering Assistant
License: MIT
SIMULATION ONLY — 無實體控制介面
"""

import numpy as np
from scipy.integrate import solve_ivp
from dataclasses import dataclass
from typing import Dict, List, Tuple

# ============================================================================
# 01 & 02: DATA GATEWAY & CELESTIAL STATE (NASA/JPL 常數)
# ============================================================================
AU = 1.495978707e8          # km
DAY_SEC = 86400.0
MU_SUN = 1.32712440018e11   # km^3/s^2
MU_EARTH = 3.986004418e5
MU_MARS = 4.282837e4

# 真實 Psyche 參數 (僅用於星曆傳播)
MU_PSYCHE_REAL = 1.601      # km^3/s^2 (Farnocchia et al. 2024)
PSYCHE_RADIUS = 113.0       # km (平均半徑)

# ============================================================================
# 實驗參數 (純數值敏感度測試)
# ============================================================================
EXPERIMENTAL_SCALE = 10000.0
MU_PSYCHE_EXP = MU_PSYCHE_REAL * EXPERIMENTAL_SCALE

# 人工數值模型階段切換半徑 (不代表真實 Psyche SOI)
EXPERIMENTAL_SWITCH_RADIUS = 500000.0

# 模擬時長限制
MAX_SIM_DAYS = 500

# ============================================================================
# 資料分類標籤
# ============================================================================
DATA_CLASS = "NON_PHYSICAL"
BODY = "16 Psyche"
REAL_MU = MU_PSYCHE_REAL
EXPERIMENTAL_MULTIPLIER = EXPERIMENTAL_SCALE
MODEL = "NON-PHYSICAL"
EPHEMERIS = "SIMPLIFIED"
MISSION_DATA = "NOT_USED_FOR_CONTROL"

SIMULATION_ONLY = True
if not SIMULATION_ONLY:
    raise RuntimeError("Safety block: Real-world deployment disabled.")

# ============================================================================
# 天體傳播器 (簡化星曆)
# ============================================================================
@dataclass
class Body:
    name: str
    mu: float
    pos: np.ndarray
    vel: np.ndarray

class SimplifiedEphemeris:
    """使用簡化模型，非真實 JPL 星曆"""
    @staticmethod
    def earth(t_sec: float) -> Body:
        a = 1.0 * AU
        n = np.sqrt(MU_SUN / a**3)
        theta = n * t_sec
        return Body("Earth", MU_EARTH,
                    np.array([a*np.cos(theta), a*np.sin(theta), 0.0]),
                    np.array([-a*n*np.sin(theta), a*n*np.cos(theta), 0.0]))

    @staticmethod
    def mars(t_sec: float) -> Body:
        """固定位置 (非真實星曆) — 僅供參考"""
        return Body("Mars", MU_MARS,
                    np.array([1.5237 * AU, 0.0, 0.0]),
                    np.array([0.0, 0.0, 0.0]))

    @staticmethod
    def psyche(t_sec: float) -> Body:
        """真實 Psyche 日心軌道 (使用真實 μ) — 此部分不受實驗倍率影響"""
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
            E = E - (E - e*np.sin(E) - M) / (1 - e*np.cos(E))

        nu = 2 * np.arctan2(np.sqrt(1+e)*np.sin(E/2), np.sqrt(1-e)*np.cos(E/2))
        r = a * (1 - e*np.cos(E))
        x_orb, y_orb = r*np.cos(nu), r*np.sin(nu)
        p = a*(1-e**2)
        vx_orb, vy_orb = -np.sqrt(MU_SUN/p)*np.sin(nu), np.sqrt(MU_SUN/p)*(e+np.cos(nu))

        cosO, sinO = np.cos(Omega), np.sin(Omega)
        cosi, sini = np.cos(i), np.sin(i)
        cosw, sinw = np.cos(w), np.sin(w)

        x = (cosO*cosw - sinO*sinw*cosi)*x_orb + (-cosO*sinw - sinO*cosw*cosi)*y_orb
        y = (sinO*cosw + cosO*sinw*cosi)*x_orb + (-sinO*sinw + cosO*cosw*cosi)*y_orb
        z = (sinw*sini)*x_orb + (cosw*sini)*y_orb
        vx = (cosO*cosw - sinO*sinw*cosi)*vx_orb + (-cosO*sinw - sinO*cosw*cosi)*vy_orb
        vy = (sinO*cosw + cosO*sinw*cosi)*vx_orb + (-sinO*sinw + cosO*cosw*cosi)*vy_orb
        vz = (sinw*sini)*vx_orb + (cosw*sini)*vy_orb

        return Body("16 Psyche", MU_PSYCHE_REAL,
                    np.array([x, y, z]), np.array([vx, vy, vz]))

# ============================================================================
# 階段 1：局部實驗場逃逸 (使用 10,000× μ)
# ============================================================================
def local_escape_simulation(sc_pos0: np.ndarray, sc_vel0: np.ndarray,
                            t_max_days: float = 30.0) -> Dict:
    """在 Psyche 局部場中積分，使用 MU_PSYCHE_EXP"""
    def derivatives(t, state):
        pos = state[0:3]
        vel = state[3:6]
        psyche = SimplifiedEphemeris.psyche(t)

        bodies = [
            Body("Sun", MU_SUN, np.zeros(3), np.zeros(3)),
            SimplifiedEphemeris.earth(t),
            SimplifiedEphemeris.mars(t),
        ]

        acc = np.zeros(3)
        for b in bodies:
            delta = b.pos - pos
            dsq = np.dot(delta, delta) + 1e-12
            d = np.sqrt(dsq)
            acc += b.mu * delta / (dsq * d)

        delta_p = psyche.pos - pos
        dsq_p = np.dot(delta_p, delta_p) + 1e-12
        d_p = np.sqrt(dsq_p)
        acc += MU_PSYCHE_EXP * delta_p / (dsq_p * d_p)

        return np.concatenate([vel, acc])

    t_span = (0.0, t_max_days * DAY_SEC)
    t_eval = np.linspace(0.0, t_max_days * DAY_SEC, 2000)
    state0 = np.concatenate([sc_pos0, sc_vel0])

    sol = solve_ivp(derivatives, t_span, state0, t_eval=t_eval,
                    method='RK45', rtol=1e-10, atol=1e-12)

    if not sol.success:
        raise RuntimeError(f"Local escape failed: {sol.message}")

    # 尋找脫離切換半徑的點
    escape_idx = None
    for i in range(len(sol.t)):
        psyche = SimplifiedEphemeris.psyche(sol.t[i])
        dist = np.linalg.norm(sol.y[0:3, i] - psyche.pos)
        if dist > EXPERIMENTAL_SWITCH_RADIUS:
            escape_idx = i
            break

    if escape_idx is None:
        escape_idx = -1
        print(f"[警告] 模擬結束仍未脫離切換半徑 (距離 {np.linalg.norm(sol.y[0:3, -1] - SimplifiedEphemeris.psyche(sol.t[-1]).pos):.0f} km)")

    return {
        "t_sec": sol.t[escape_idx],
        "pos": sol.y[0:3, escape_idx],
        "vel": sol.y[3:6, escape_idx],
        "psyche_pos": SimplifiedEphemeris.psyche(sol.t[escape_idx]).pos,
        "dist_to_psyche": np.linalg.norm(sol.y[0:3, escape_idx] - SimplifiedEphemeris.psyche(sol.t[escape_idx]).pos),
        "full_sol": sol
    }

# ============================================================================
# 階段 2：日心轉移 (真實太陽重力)
# ============================================================================
def heliocentric_transfer(pos0: np.ndarray, vel0: np.ndarray,
                          t0_sec: float, max_days: float = 400.0) -> Dict:
    """從脫離點開始，僅受太陽重力，追蹤 1 AU 穿越"""
    def derivatives(t, state):
        pos = state[0:3]
        vel = state[3:6]
        r = np.linalg.norm(pos)
        acc = -MU_SUN * pos / (r**3 + 1e-12)
        return np.concatenate([vel, acc])

    t_span = (0.0, max_days * DAY_SEC)
    t_eval = np.linspace(0.0, max_days * DAY_SEC, 50000)
    state0 = np.concatenate([pos0, vel0])

    sol = solve_ivp(derivatives, t_span, state0, t_eval=t_eval,
                    method='RK45', rtol=1e-10, atol=1e-12)

    if not sol.success:
        raise RuntimeError(f"Heliocentric transfer failed: {sol.message}")

    crossing_idx = None
    for i in range(1, len(sol.t)):
        r_prev = np.linalg.norm(sol.y[0:3, i-1])
        r_curr = np.linalg.norm(sol.y[0:3, i])
        if (r_prev > AU and r_curr < AU) or (r_prev < AU and r_curr > AU):
            crossing_idx = i
            break

    if crossing_idx is None:
        print("[警告] 模擬結束未穿越 1 AU")
        crossing_idx = -1

    t_cross = sol.t[crossing_idx] + t0_sec
    earth_at_cross = SimplifiedEphemeris.earth(t_cross)
    sc_at_cross = sol.y[0:3, crossing_idx]
    dist_to_earth = np.linalg.norm(sc_at_cross - earth_at_cross.pos)

    return {
        "cross_time_sec": sol.t[crossing_idx],
        "cross_time_days": sol.t[crossing_idx] / DAY_SEC,
        "cross_pos": sol.y[0:3, crossing_idx],
        "cross_vel": sol.y[3:6, crossing_idx],
        "earth_pos_at_cross": earth_at_cross.pos,
        "earth_dist_km": dist_to_earth,
        "full_sol": sol,
        "crossing_detected": crossing_idx != -1
    }

# ============================================================================
# 主執行流程
# ============================================================================
if __name__ == "__main__":
    print("=" * 70)
    print("        GRAVITY-FLOAT v4 — NON-PHYSICAL EXPERIMENT")
    print("=" * 70)
    print(f"資料分類 : {DATA_CLASS}")
    print(f"目標天體 : {BODY}")
    print(f"真實 μ   : {REAL_MU:.3f} km³/s²")
    print(f"實驗倍率 : {EXPERIMENTAL_MULTIPLIER:.0f}×")
    print(f"實驗 μ   : {MU_PSYCHE_EXP:.1f} km³/s²")
    print(f"切換半徑 : {EXPERIMENTAL_SWITCH_RADIUS:,.0f} km (人工數值模型)")
    print("⚠️  純數值模擬 | 無實體控制 | 嚴禁解讀為真實任務時間\n")

    # ----- 初始條件：逃逸速度出發 -----
    psyche_initial = SimplifiedEphemeris.psyche(0.0)
    sc_init_pos = psyche_initial.pos + np.array([PSYCHE_RADIUS + 500.0, 0.0, 0.0])
    # 修正：初始相對速度設為 10,000× μ 下的逃逸速度 (約 7.23 km/s)
    v_esc = np.sqrt(2 * MU_PSYCHE_EXP / (PSYCHE_RADIUS + 500.0))
    sc_init_vel = psyche_initial.vel + np.array([v_esc, 0.0, 0.0])

    print(f"[初始條件] 半徑 : {PSYCHE_RADIUS + 500.0:.0f} km")
    print(f"            逃逸速度 : {v_esc:.4f} km/s")

    # ----- 階段 1 -----
    print("\n[階段 1] 局部實驗場逃逸模擬...")
    local_result = local_escape_simulation(sc_init_pos, sc_init_vel, t_max_days=30.0)

    t_escape_days = local_result["t_sec"] / DAY_SEC
    dist_escape = local_result["dist_to_psyche"]
    pos_escape = local_result["pos"]
    vel_escape = local_result["vel"]

    v_rel = np.linalg.norm(vel_escape - SimplifiedEphemeris.psyche(local_result["t_sec"]).vel)
    epsilon = (v_rel**2 / 2) - (MU_PSYCHE_EXP / dist_escape)

    print(f"  逃逸時間   : {t_escape_days:.2f} 天")
    print(f"  逃逸距離   : {dist_escape:,.0f} km")
    print(f"  相對速度   : {v_rel:.4f} km/s")
    print(f"  比軌道能量 : {epsilon:.4f} km²/s²")
    print(f"  狀態       : {'INSTANTANEOUS_BOUND' if epsilon < 0 else 'INSTANTANEOUS_UNBOUND'}")

    # ----- 階段 2 -----
    print("\n[階段 2] 切換至真實太陽重力場，追蹤 1 AU 穿越...")
    transfer_result = heliocentric_transfer(pos_escape, vel_escape,
                                            t0_sec=local_result["t_sec"],
                                            max_days=500.0)

    if transfer_result["crossing_detected"]:
        print(f"\n[穿越 1 AU]")
        print(f"  發生時間   : {transfer_result['cross_time_days']:.2f} 天 (自逃逸起算)")
        print(f"  探測器位置 : ({transfer_result['cross_pos'][0]:.0f}, {transfer_result['cross_pos'][1]:.0f}) km")
        print(f"  地球位置   : ({transfer_result['earth_pos_at_cross'][0]:.0f}, {transfer_result['earth_pos_at_cross'][1]:.0f}) km")
        print(f"  與地球距離 : {transfer_result['earth_dist_km']:,.0f} km")
    else:
        print("\n[穿越 1 AU] 未偵測到穿越")

    # ----- 結論 -----
    print("\n" + "=" * 70)
    print("                   最終診斷結論")
    print("=" * 70)
    if transfer_result["crossing_detected"]:
        print(f"✅ 探測器在 {transfer_result['cross_time_days']:.1f} 天內穿越 1 AU。")
        print(f"   穿越時距離地球 {transfer_result['earth_dist_km']:,.0f} km。")
        print("   (此為理想化二體太陽轉移，未計行星攝動)")
    else:
        print("❌ 探測器未能在 500 天內穿越 1 AU。")

    print(f"\n[安全] {DATA_CLASS} | SIMULATION_ONLY = True")
    print(f"[模型] {MODEL} | 星曆: {EPHEMERIS}")
    print(f"[任務] {MISSION_DATA}")
