import numpy as np
from astropy import units as u
from astropy.units import Quantity as Q

from ..virial import Virial


class NFW():
    def __init__(self, rho_0: Q["mass density"], r_0: Q["length"], virial=None):
        self.rho_0: Q["mass density"] = rho_0
        self.r_0: Q["length"] = r_0

        if virial is not None:
            self.set_virial(virial)
        else:
            self.virial = None
            self.r_vir = None
            self.M_vir = None
            self.c = None

    def __repr__(self):
        return f"NFW(rho_0={self.rho_0:.3e}, r_0={self.r_0:.3e})"

    def density(self, r: Q["length"]):
        x = (r / self.r_0).to(u.dimensionless_unscaled)
        return self.rho_0 / (x * (1 + x)**2)

    def enclosed_mass(self, r: Q["length"]):
        x = (r / self.r_0).to(u.dimensionless_unscaled)
        return 4 * np.pi * self.rho_0 * self.r_0**3 * self._f(x)

    def set_virial(self, virial):
        self.virial = virial
        self.r_vir = self.virial.find_radius(self)
        self.M_vir = self.virial.M_vir(self.r_vir)
        self.c     = self.r_vir / self.r_0

    def virial_radius(self):
        if self.virial is None: raise ValueError("Virial parameters not set.")
        return self.r_vir

    def virial_mass(self):
        if self.virial is None: raise ValueError("Virial parameters not set.")
        return self.M_vir

    def concentration(self):
        if self.virial is None: raise ValueError("Virial parameters not set.")
        return self.c

    @staticmethod
    def _f(x):
        return np.log(1 + x) - x / (1 + x)

    @staticmethod
    def from_virial_mass(M_vir: Q["mass"], c_vir: float, virial=None):
        """Create an NFW profile from a virial mass and concentration."""
        if virial is None:
            virial = Virial()

        r_vir = virial.r_vir(M_vir)
        r_0 = r_vir / c_vir
        rho_0 = M_vir / (4 * np.pi * r_0**3 * NFW._f(c_vir))
        return NFW(rho_0, r_0, virial)
