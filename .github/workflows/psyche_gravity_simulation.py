"""
Module: psyche_gravity_simulation.py
Description: Accurate gravitational force and surface gravity calculation 
             for asteroid 16 Psyche based on NASA/JPL parameters (2024–2026 data).
"""

import numpy as np
from dataclasses import dataclass

@dataclass
class CelestialBody:
    name: str
    mass: float          # kg
    mean_radius: float   # m

class PsycheGravityEngine:
    G = 6.67430e-11  # m^3 kg^-1 s^-2

    def __init__(self):
        # Updated parameters (Farnocchia et al. 2024 & NASA mission data)
        self.psyche = CelestialBody(
            name="16 Psyche",
            mass=2.40e19,           # kg
            mean_radius=113_000.0   # m (≈226 km diameter)
        )
        self.arrival_window = "2029-07 (capture) / 2029-08 (science orbit)"

    def surface_gravity(self) -> float:
        """Calculate surface gravitational acceleration (m/s²)."""
        return self.G * self.psyche.mass / self.psyche.mean_radius**2

    def gravitational_acceleration(self, altitude_m: float) -> float:
        """Gravitational acceleration at given altitude above surface (m/s²)."""
        r = self.psyche.mean_radius + altitude_m
        return self.G * self.psyche.mass / r**2

    def force_on_spacecraft(self, spacecraft_mass_kg: float, altitude_m: float) -> float:
        """Gravitational force exerted on spacecraft (N)."""
        return spacecraft_mass_kg * self.gravitational_acceleration(altitude_m)

    def euclidean_distance(self, pos1: np.ndarray, pos2: np.ndarray) -> float:
        """Instantaneous distance between two position vectors (km)."""
        return np.linalg.norm(pos2 - pos1)

# --- Execution Example ---
if __name__ == "__main__":
    engine = PsycheGravityEngine()

    print(f"Target: {engine.psyche.name}")
    print(f"Estimated arrival: {engine.arrival_window}")
    print(f"Surface gravity: {engine.surface_gravity():.4f} m/s²")
    print(f"Acceleration at 500 km altitude: {engine.gravitational_acceleration(500_000):.6f} m/s²")
    print(f"Force on 2000 kg spacecraft at 500 km: {engine.force_on_spacecraft(2000, 500_000):.4f} N")

    # Example dynamic distance (mock positions in km; replace with real ephemeris for precision)
    earth_pos = np.array([1.496e8, 0.0, 0.0])
    psyche_pos = np.array([3.0e8, 5.0e7, 1.0e6])  # illustrative
    dist = engine.euclidean_distance(earth_pos, psyche_pos)
    print(f"Illustrative Earth–Psyche distance: {dist:,.0f} km")
