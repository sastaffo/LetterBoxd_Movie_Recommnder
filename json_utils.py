import json


def read_from_file(filepath):

    # data = None

    with open(filepath) as fp:
        data = json.load(fp)

    return data


def write_to_file(data, filepath):

    with open(filepath, 'w') as fp:
        fp.write(json.dumps(data))
