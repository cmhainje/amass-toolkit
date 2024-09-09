import numpy as np
import h5py

from os.path import exists
from astropy import units as u

class Snapshot():
    def __init__(self, path):
        if not exists(path):
            raise FileNotFoundError(f"Snapshot file not found: {path}")

        self.path = path
        with h5py.File(self.path, 'r') as f:
            self.header = dict(f['Header'].attrs)

        self.time = float(self.header['Time'])
        self.num_particles = np.array(self.header['Npart'])

        self._read_units()

    def __repr__(self):
        return f"Snapshot({self.path})"

    def _read_units(self):
        # read the code units from the header and make them into astropy units
        self.u_length      = u.def_unit('code_length',      self.header['UnitLength_in_cm'] * u.cm)
        self.u_mass        = u.def_unit('code_mass',        self.header['UnitMass_in_g'] * u.g)
        self.u_velocity    = u.def_unit('code_velocity',    self.header['UnitVelocity_in_cm_per_s']) * u.cm / u.s)
        self.u_mag_field   = u.def_unit('code_mag_field',   self.header['UnitMagneticField_in_gauss)'] * u.G)
        self.u_time        = u.def_unit('code_time',        self.u_length / self.u_velocity)
        self.u_spec_energy = u.def_unit('code_spec_energy', self.u_velocity ** 2)
        self.u_density     = u.def_unit('code_density',     self.u_mass / self.u_length ** 3)
        self.u_div_damp    = u.def_unit('code_div_damp',    self.u_mag_field * self.u_velocity)

    def _make_sort_indices(self):
        self.sort_idx = dict()
        with h5py.File(self.path, 'r') as f:
            for i, n in enumerate(self.num_particles):
                if n == 0:
                    continue
                ids = f[f'PartType{i}/ParticleIDs'][:]
                self.sort_idx[i] = np.argsort(ids)

    def __getitem__(self, key):
        with h5py.File(self.path, 'r') as f:
            x = f[f'PartType{part_type}/{key}'][:]
        return x[self.sort_idx[part_type]]

    def get_position(self, part_type):
        with h5py.File(self.path, 'r') as f:
            pos = f[f'PartType{part_type}/Coordinates'][:]
        return pos[self.sort_idx[part_type]]

    def get_velocity(self, part_type):
        with h5py.File(self.path, 'r') as f:
            vel = f[f'PartType{part_type}/Velocities'][:]
        return vel[self.sort_idx[part_type]]

    def get_mass(self, part_type):
        with h5py.File(self.path, 'r') as f:
            mass = f[f'PartType{part_type}/Masses'][:]
        return mass[self.sort_idx[part_type]]
