from os.path import exists

def read_paramfile(path):
    """Reads a parameter file and returns a dict of all specified parameters.

    Designed to work with GADGET-like paramfiles, where each line is a key-value pair
    separated by whitespace. Comments are allowed and start with a '%' character."""

    if not exists(path):
        raise FileNotFoundError(f"Parameter file not found: {path}")
    with open(path, "r") as f:
        lines = f.readlines()

    params = {}

    for line in lines:
        line = line.strip()
        if line == '' or line.startswith('%'):
            # skip empty lines and comments
            continue

        # split with 'None' to split on any whitespace
        key, value = line.split(None, 1)

        # try to parse as int
        try:
            value = int(value)
        except ValueError:
            # try to parse as float
            try:
                value = float(value)
            except ValueError:
                # leave as string
                pass

        params[key] = value

    return params
