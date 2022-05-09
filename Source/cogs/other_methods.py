import json
from datetime import datetime


def load_config(path: str) -> dict:
    """
    Function load_config takes a JSON file, loads it and returns the 
    object as dictionary.

    Parameters
    ----------
    path : str
        path to JSON file.visu.
    """
    with open(path, encoding='utf8') as cfg:
        config = json.load(cfg)
    return config


def current_time() -> int:
    """This function returns the current time as timestamp (integer)"""
    return int(datetime.timestamp(datetime.now()))
