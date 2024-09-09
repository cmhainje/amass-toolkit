import numpy as np
from scipy.optimize import root_scalar
from astropy import units as u
from astropy.units import Quantity as Q
from astropy import cosmology as cosmo

from .units import default_units

class Virial():
    def __init__(self, redshift=0, cosmology=None, overdensity=200):
        if cosmology is None:
            cosmology = cosmo.default_cosmology.get()

        self.cosmology = cosmology
        self.redshift = redshift

        self.H = self.cosmology.H(self.redshift)
        self.rho_c = self.cosmology.critical_density(self.redshift)
        self.overdensity = overdensity
        self.rho_vir = self.overdensity * self.rho_c

    def __repr__(self):
        return f"Virial(redshift={self.redshift}, overdensity={self.overdensity}, cosmology={self.cosmology})"

    def r_vir(self, M: Q["mass"]) -> Q["length"]:
        """Calculate the virial radius of a halo with mass M."""
        r = (3 * M / (4 * np.pi * self.rho_vir))**(1/3)
        return r.to(default_units["length"])

    def M_vir(self, r: Q["length"]) -> Q["mass"]:
        """Calculate the virial mass of a halo with radius r."""
        m = 4 * np.pi * self.rho_vir * r**3 / 3
        return m.to(default_units["mass"])

    def find_radius(self, density_profile, min_radius=1e-3, max_radius=1e3) -> Q["length"]:
        """Find the radius at which the average density inside the density
        profile is equal to the overdensity threshold."""

        r_unit = density_profile.r_0.unit
        r_0    = density_profile.r_0.value

        def rho_diff(r: float):
            rho = density_profile.density(r * r_unit).to(self.rho_vir.unit)
            return (rho - self.rho_vir).value

        r = root_scalar(rho_diff, bracket=[r_0 * min_radius, r_0 * max_radius]).root
        return r * r_unit
