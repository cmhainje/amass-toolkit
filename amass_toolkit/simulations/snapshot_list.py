import numpy as np

from os.path import exists, join
from glob import glob

from .snapshot import Snapshot

class SnapshotList():
    def __init__(
        self,
        path,
        snap_prefix="snapshot",
        snap_suffix=".hdf5"
    ):
        if not exists(path):
            raise FileNotFoundError(f"Simulation not found at {path}")

        self.path = path

        # find all snapshot files
        snapshots = glob(join(self.path, f"{snap_prefix}*{snap_suffix}"))
        if len(snapshots) == 0:
            raise FileNotFoundError(f"No snapshots found at {path}")

        self.snapshots = [ Snapshot(s) for s in snapshots ]
        self.snapshots = sorted(self.snapshots, key=lambda s: s.time)
        self.times = np.array([ s.time for s in self.snapshots ])
