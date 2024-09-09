import numpy as np
from astropy import units as u
from astropy.units import Quantity as Q

class Hernquist():
    def __init__(self, rho_0: Q["mass density"], r_0: Q["length"]):
        self.rho_0: Q["mass density"] = rho_0
        self.r_0: Q["length"] = r_0
        pass

    def density(self, r: Q["length"]):
        x = (r / self.r_0).to(u.dimensionless_unscaled)
        return self.rho_0 / (x * (1 + x)**3)

    def enclosed_mass(self, r: Q["length"]):
        x = (r / self.r_0).to(u.dimensionless_unscaled)
        return 2 * np.pi * self.rho_0 * self.r_0**3 * x**2 / (1 + x)**2
