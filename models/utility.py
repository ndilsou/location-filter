import gzip
import json
import os

import pandas as pd
import random

import re
import jsonlines

PATTERN = re.compile("www\.| |\.com|\.co\.uk|\.org|\.uk|\.ie|\.net")


def get_current_file_directory():
    return os.path.dirname(__file__)

def load_dataset():
    """
    load the articles, annotations and locations data as lists of dictionaries.
    :return: articles, annotations, locations
    """
    cwd = os.path.dirname(__file__)
    parent_dir = os.path.dirname(cwd)
    with gzip.open(os.path.join(parent_dir, "data/articles.jl.gz"), "rb") as fh:
        with jsonlines.Reader(fh) as reader:
            raw_articles = [item for item in reader]
            print(f"articles count: {len(raw_articles)}")

    with gzip.open(os.path.join(parent_dir, "data/annotations.jl.gz"), "rb") as fh:
        with jsonlines.Reader(fh) as reader:
            raw_annotations = [item for item in reader]
            print(f"annotations count: {len(raw_annotations)}")

    with gzip.open(os.path.join(parent_dir, "data/locations.jl.gz"), "rb") as fh:
        with jsonlines.Reader(fh) as reader:
            raw_locations = [item for item in reader]
            print(f"locations count: {len(raw_locations)}")

    return raw_articles, raw_annotations, raw_locations


def summarize_text(text, start=30, end=10):
    """
    Shorten a long text for easy display.
    :param text: the original text.
    :param start: Length of the first block.
    :param end: Length of the end block.
    :return: The shortened text.
    """
    if len(text) > (start + end):
        summary = f"{text[:start]}...{text[-end:]}"
    else:
        summary = text
    return summary


def pretty_dict(d):
    """
    provide a stringified and indented view of a dictionary.
    :param d: the original dictionary.
    :return:
    """
    return json.dumps(d, indent=4)


def clean_publisher(publisher):
    """
    Clean the name of a publisher.
    :param publisher:
    :return:
    """
    # clean websites name
    # Note that using split may have us miss names like edinburghnews.scotsman.com
    publisher = PATTERN.sub("", publisher)
    publisher = publisher.lower()
    return publisher


def get_location_index(locations):
    """
    provides a mapping from location_index to location in the dataset.
    :param locations: the location dataset.
    :return:
    """
    return {l["id"]: i for i, l in enumerate(locations)}


def get_article_to_loc_index(articles, locations, uri_index):
    pass


def get_annotation_uri_index(annotations, locations):
    """
    provides a dictionary mapping from the annotation_uri to the annotation and all locations pointing to it.
    :return:
    """
    uri_index = {a["uri"]: {"annotation": a, "locations": []} for a in annotations}
    for location in locations:
        for uri in location["annotation_uri"]:
            uri_index.get(uri, {"annotation": None, "locations": []})["locations"].append(location)
    return uri_index


def sample_locations(locations, k, known_loc_ids):
    """
    Provides a sample of locations ids that are out of the set of known locations.
    Use this method to form the negative part of your sample.

    :param locations: the list of raw locations.
    :param k:
    :param known_loc_ids:
    :return:
    """
    location_index = get_location_index(locations)
    all_ids = set(location_index.keys())
    acceptable_ids = all_ids.difference(known_loc_ids)
    return random.choices(list(acceptable_ids), k=k)


def get_loc_features(selected_ids, locations, features):
    """
    returns the dataframe of features for the selected location ids.
    :param selected_ids:
    :param location_index:
    :param locations:
    :param features:
    :return:
    """

    geo_loc = []
    location_index = get_location_index(locations)
    for loc_id in selected_ids:
        location = locations[location_index[loc_id]]
        geo_loc.append((loc_id, *(location[f] for f in features)))
    geo_loc = pd.DataFrame(geo_loc, columns=["lat", "lng", "id"])
    return geo_loc


def get_dummies(frame, col, return_columns=False):
    """
    Replaces a categorical column in the target frame by a set of one-hot encoded columns.
    :param frame: the target pandas DataFrame.
    :param col: the column to one-hot encode.
    :return: the dataframe with the one-hot encoded columns added and the original column dropped.
    """

    one_hot_encoded = pd.get_dummies(frame[col])
    encoded_columns = one_hot_encoded.columns
    one_hot_encoded = pd.concat((frame, one_hot_encoded), axis=1)
    if return_columns:
        return one_hot_encoded.drop(col, axis=1), encoded_columns
    else:
        return one_hot_encoded.drop(col, axis=1)
