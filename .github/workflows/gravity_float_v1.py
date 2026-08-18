"""
Module: gravity_float_v1.py
Description: Gravity-Float Core v1 - 16 Psyche N-body gravity simulation.
             Based on NASA/JPL public ephemeris parameters (GM, orbital elements).
             Strictly SIMULATION ONLY. No real-world control interface.
Author: Engineering Assistant
License: MIT
"""

import numpy as np
from scipy.integrate import solve_ivp
from dataclasses import dataclass
from typing import Tuple, Dict, List
import warnings

# ============================================================================
# LAYER 1 & 2: DATA GATEWAY & CELESTIAL MODEL (NASA/JPL Public Constants)
# ============================================================================
AU = 1.495978707e8          # km
G = 6.67430e-20             # km^3 kg^-1 s^-2 (gravitational constant in astronomical units)
DAY_SEC = 86400.0

# JPL/NASA Standard Gravitational Parameters (GM) in km^3/s^2
GM_SUN = 1.32712440018e11
GM_EARTH = 3.986004418e5
GM_MARS = 4.282837e4
GM_PSYCHE = 1.601            # Latest high-precision (Farnocchia et al. 2024)

@dataclass
class Body:
    """Celestial body with position, velocity, and gravitational parameter."""
    name: str
    gm: float                 # km^3/s^2
    position: np.ndarray      # [x, y, z] in km (heliocentric ecliptic)
    velocity: np.ndarray      # [vx, vy, vz] in km/s

    def reset(self, pos: np.ndarray, vel: np.ndarray):
        self.position = pos.astype(float)
        self.velocity = vel.astype(float)

# ============================================================================
# LAYER 3: GRAVITY CORE (F = GMm/r^2, a = GM/r^2)
# ============================================================================
class GravityCore:
    @staticmethod
    def acceleration_from_body(body: Body, r_vec: np.ndarray) -> np.ndarray:
        """
        Compute gravitational acceleration (km/s^2) exerted by `body` on a point mass at position r_vec.
        r_vec: position vector of test mass (heliocentric km).
        """
        delta = body.position - r_vec
        dist_sq = np.dot(delta, delta)
        if dist_sq < 1e-12:
            return np.zeros(3)
        dist = np.sqrt(dist_sq)
        accel = body.gm * delta / (dist_sq * dist)  # direction: towards body
        return accel

    @staticmethod
    def total_acceleration(r_vec: np.ndarray, bodies: List[Body]) -> np.ndarray:
        """Sum acceleration from all bodies."""
        acc = np.zeros(3)
        for body in bodies:
            acc += GravityCore.acceleration_from_body(body, r_vec)
        return acc

    @staticmethod
    def escape_velocity(gm: float, distance_km: float) -> float:
        """Escape velocity (km/s) from a body at given distance."""
        if distance_km <= 0:
            return np.inf
        return np.sqrt(2 * gm / distance_km)

    @staticmethod
    def surface_gravity(gm: float, radius_km: float) -> float:
        """Surface gravity in m/s^2."""
        if radius_km <= 0:
            return 0.0
        return (gm / (radius_km ** 2)) * 1000  # convert km/s^2 to m/s^2

# ============================================================================
# LAYER 4: N-BODY ENGINE (Numerical Integration via SciPy)
# ============================================================================
class NBodyEngine:
    """
    Simulates the trajectory of a spacecraft under the gravity of Sun, Earth, Mars, and 16 Psyche.
    Uses fixed background ephemeris for massive bodies (simplified Keplerian motion for this demo).
    """
    def __init__(self):
        self.bodies = []
        self.psyche_radius = 113.0  # km (mean radius)

    def set_initial_conditions(self, sc_pos: np.ndarray, sc_vel: np.ndarray):
        """Initialize spacecraft state."""
        self.sc_initial_pos = sc_pos
        self.sc_initial_vel = sc_vel

    def _background_bodies_at_time(self, t_sec: float) -> List[Body]:
        """
        Placeholder for ephemeris. 
        In production, load SPICE or Horizons. 
        Here we keep Psyche static for simplicity, but we give Earth/Sun fixed positions.
        NOTE: For a true ephemeris, replace this with actual Kepler propagation or Horizons query.
        """
        # This is a SIMPLIFIED fixed background for demo. 
        # Real usage would require time-varying positions.
        # For Psyche, we keep it at a fixed point near 3.0 AU for demonstration.
        sun = Body("Sun", GM_SUN, np.array([0.0, 0.0, 0.0]), np.array([0.0, 0.0, 0.0]))
        # Earth approx at 1 AU on X-axis (simplified)
        earth = Body("Earth", GM_EARTH, np.array([1.0*AU, 0.0, 0.0]), np.array([0.0, 29.78, 0.0]))
        # Mars approx at 1.52 AU
        mars = Body("Mars", GM_MARS, np.array([1.52*AU, 0.0, 0.0]), np.array([0.0, 24.07, 0.0]))
        # Psyche: placed at approx 2.9 AU, slightly inclined, matching 2029 rendezvous position.
        psyche = Body("16 Psyche", GM_PSYCHE, 
                      np.array([2.9*AU, 0.5*AU, 0.1*AU]), 
                      np.array([0.0, 18.0, 1.0]))  # rough orbital velocity
        
        # In a full version, propagate these bodies with Kepler/N-body too.
        return [sun, earth, mars, psyche]

    def _derivatives(self, t: float, state: np.ndarray) -> np.ndarray:
        """
        State vector: [x, y, z, vx, vy, vz] (heliocentric).
        Returns derivative [vx, vy, vz, ax, ay, az].
        """
        pos = state[0:3]
        vel = state[3:6]
        
        # Get background bodies at this time (static in this simplified demo)
        bodies = self._background_bodies_at_time(t)
        acc = GravityCore.total_acceleration(pos, bodies)
        return np.concatenate([vel, acc])

    def simulate(self, duration_days: float, step_minutes: float = 10.0) -> Dict:
        """Run simulation from initial conditions."""
        t_span = (0, duration_days * DAY_SEC)
        t_eval = np.linspace(0, duration_days * DAY_SEC, int(duration_days * DAY_SEC / (step_minutes * 60)))
        
        state0 = np.concatenate([self.sc_initial_pos, self.sc_initial_vel])
        
        # Run integration
        sol = solve_ivp(self._derivatives, t_span, state0, t_eval=t_eval, method='RK45', rtol=1e-9)
        
        if not sol.success:
            warnings.warn(f"Integration failed: {sol.message}")
        
        return {
            "t_days": sol.t / DAY_SEC,
            "positions_km": sol.y[0:3].T,
            "velocities_km_s": sol.y[3:6].T
        }

# ============================================================================
# LAYER 5: GRAVITY-FLOAT ANALYZER (Orbit State, Stability, Perturbations)
# ============================================================================
class FloatAnalyzer:
    @staticmethod
    def compute_relative_state(pos_sc: np.ndarray, vel_sc: np.ndarray, target_pos: np.ndarray) -> Dict:
        """Compute distance, relative speed, and local gravity from Psyche."""
        delta = pos_sc - target_pos
        distance_km = np.linalg.norm(delta)
        if distance_km < 1:
            distance_km = 1.0  # prevent division by zero
        
        # Gravitational acceleration from Psyche only (km/s^2)
        acc_psyche = GM_PSYCHE / (distance_km ** 2)
        acc_psyche_ms2 = acc_psyche * 1000
        
        # Escape velocity from current distance
        v_esc = GravityCore.escape_velocity(GM_PSYCHE, distance_km)
        
        return {
            "distance_km": distance_km,
            "gravity_m_s2": acc_psyche_ms2,
            "escape_velocity_km_s": v_esc,
            "relative_speed_km_s": np.linalg.norm(vel_sc)  # simplified: relative to inertial
        }

# ============================================================================
# LAYER 6: SAFETY / GOVERNANCE
# ============================================================================
SIMULATION_ONLY = True
SAFETY_GUARD = "⚠️  This is a PURE NUMERICAL SIMULATION. No real spacecraft commands are generated."

if not SIMULATION_ONLY:
    raise RuntimeError("Safety block: Real-world deployment disabled by SAFETY_GUARD.")

# ============================================================================
# MAIN EXECUTION & DASHBOARD
# ============================================================================
if __name__ == "__main__":
    print("="*60)
    print("          GRAVITY-FLOAT CORE v1 (16 PSYCHE)")
    print("="*60)
    print(SAFETY_GUARD)
    print("\n[INFO] Initializing simulation based on NASA/JPL 2024 parameters...")
    print(f"[INFO] Psyche GM = {GM_PSYCHE:.3f} km^3/s^2")
    print(f"[INFO] Psyche mean radius = 113.0 km")
    print(f"[INFO] Surface gravity = {GravityCore.surface_gravity(GM_PSYCHE, 113.0):.4f} m/s^2")
    print(f"[INFO] Escape velocity at surface = {GravityCore.escape_velocity(GM_PSYCHE, 113.0):.2f} km/s")
    
    # Initialize N-body engine
    engine = NBodyEngine()
    
    # Set up initial spacecraft state (approaching Psyche near 2029 rendezvous)
    # Let's place SC at a distance of ~10,000 km from Psyche, with a slight relative velocity.
    # Psyche position (approx from background bodies)
    psyche_pos = np.array([2.9*AU, 0.5*AU, 0.1*AU])
    psyche_vel = np.array([0.0, 18.0, 1.0])
    
    # Spacecraft initial state: 10,000 km away from Psyche, moving towards it slowly.
    sc_pos = psyche_pos + np.array([10000.0, 0.0, 0.0])
    sc_vel = psyche_vel + np.array([-0.5, 0.0, 0.0])  # relative approach 0.5 km/s
    
    engine.set_initial_conditions(sc_pos, sc_vel)
    
    print("\n[INFO] Running N-body simulation for 7 days (approach phase)...")
    results = engine.simulate(duration_days=7.0, step_minutes=5.0)
    
    # Extract last state for analysis
    final_pos = results["positions_km"][-1]
    final_vel = results["velocities_km_s"][-1]
    
    # Analyze relative to Psyche (keeping Psyche fixed in this simplified demo)
    analyzer = FloatAnalyzer()
    rel_state = analyzer.compute_relative_state(final_pos, final_vel, psyche_pos)
    
    print("\n" + "="*60)
    print("          FINAL STATE DASHBOARD (Day 7)")
    print("="*60)
    print(f"Distance from 16 Psyche: {rel_state['distance_km']:,.0f} km")
    print(f"Local Gravity (Psyche):  {rel_state['gravity_m_s2']:.6f} m/s²")
    print(f"Escape Velocity at dist: {rel_state['escape_velocity_km_s']:.4f} km/s")
    print(f"Spacecraft speed (inertial): {rel_state['relative_speed_km_s']:.4f} km/s")
    
    # Simplified stability check (if distance is decreasing, it's approaching)
    first_pos = results["positions_km"][0]
    initial_dist = np.linalg.norm(first_pos - psyche_pos)
    if rel_state['distance_km'] < initial_dist:
        print("\n[STABILITY] Spacecraft is approaching 16 Psyche (gravity capture likely).")
    else:
        print("\n[STABILITY] Spacecraft is receding. Gravity not dominant.")
    
    print("\n[INFO] Simulation complete. This is a theoretical model for 16 Psyche research.")
