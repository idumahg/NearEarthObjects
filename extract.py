"""Extract data on near-Earth objects and close approaches from files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the
command line, and uses the resulting collections to build an `NEODatabase`.

"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file with data on near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    neo_list = []
    with open(neo_csv_path, 'r') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            if row["pha"] == 'Y':
                neo = NearEarthObject(pdes=row["pdes"], name=row["name"],
                                      diameter=row["diameter"], pha=True)
            else:
                neo = NearEarthObject(pdes=row["pdes"], name=row["name"],
                                      diameter=row["diameter"], pha=False)
            neo_list.append(neo)
    return neo_list


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file with data on close approaches.
    :return: A collection of `CloseApproach`es.
    """
    ca_list = []
    with open(cad_json_path, 'r') as infile:
        contents = json.load(infile)
        cad_data = contents["data"]
        for entry in cad_data:
            ca = CloseApproach(des=entry[0], cd=entry[3], dist=entry[4],
                               v_rel=entry[7])
            ca_list.append(ca)
    return ca_list
