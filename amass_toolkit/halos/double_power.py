import numpy as np

from astropy import units as u
from astropy.units import Quantity as Q


class DoublePowerLaw():
    def __init__(
        self,
        scale_density: Q["mass density"],
        scale_radius: Q["length"],
        alpha: float,
        beta:  float,
        gamma: float,
    ):
        self.rho_0 = scale_density
        self.r_0   = scale_radius

        self.alpha = alpha
        self.beta  = beta
        self.gamma = gamma

        self.power_1 = -gamma
        self.power_2 = (gamma - beta) / alpha

    def density(self, r: Q["length"]):
        x = (r / self.r_0).to(u.dimensionless_unscaled)
        return self.rho_0 * (x ** self.power_1) * (1 + x**self.alpha) ** self.power_2
