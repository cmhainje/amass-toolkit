"""set default units"""

from astropy import units as u

base_units = {
    'mass': u.solMass,
    'length': u.kpc,
    'velocity': u.km / u.s,
    'time': u.Gyr,
}

derived_units = {
    'density': base_units['mass'] / base_units['length']**3,
}

default_units = {**base_units, **derived_units}
