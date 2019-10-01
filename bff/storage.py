import json
import logging
import os
from os.path import expanduser


logger = logging.getLogger(__name__)
save_dir = os.path.join(expanduser("~"), "botsforfuture")


def save(filename, **values):
    """Save the given `values` in a file with the given `filename`. This overwrites the file."""
    with open(os.path.join(save_dir, filename), "w") as f:
        json.dump(values, f)

def load(filename, key=None):
    """
    Load previously saved values from the file.
    
    If `key` is `None`, a dictionary with all values is returned.
    Otherwise, only the value of the given `key` is returned.
    """
    with open(os.path.join(save_dir, filename), "r") as f:
        data = json.load(f)
    if key:
        return data[key]
    return data
