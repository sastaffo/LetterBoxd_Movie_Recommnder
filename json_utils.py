"""
@author: Shaun
"""

import json


def read_from_file(filepath):
    """
    Read json from the filepath given
    """

    with open(filepath) as fp:
        data = json.load(fp)

    return data


def write_to_file(data, filepath):
    """
    Write json data to the filepath given
    """


    with open(filepath, 'w') as fp:
        fp.write(json.dumps(data))
