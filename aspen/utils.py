import glob
import logging
import os
import re
from datetime import datetime as dt
import urllib
import json
from urllib.parse import urlparse
from time import sleep
from numpy import random

from google.oauth2 import service_account


create_datetime = {"MM/DD/YYYY": lambda x: dt.strptime(x, "%m/%d/%Y")}

format_datetime = {"YYYY/MM/DD": lambda x: x.strftime("%Y/%m/%d")}

strip_text = lambda text: "_".join(text.strip().split(" ")).lower()


def build_url(base, **params):
    return f"{base}?{urllib.parse.urlencode(params)}"


def create_folder(file_name):

    folders = file_name.split("/")

    if len(folders) > 1:

        previous_folder = None
        for folder in folders[:-1]:

            if not previous_folder:
                previous_folder = folder

                logging.info(f"Creating folder {folder}")
                try:
                    os.mkdir(folder)
                except FileExistsError:
                    pass

            else:
                previous_folder += f"/{folder}"

                try:
                    logging.info(f"Creating folder {folder}")
                    os.mkdir(previous_folder)
                except FileExistsError:
                    pass


def create_shard(file_name, number):
    *path, extension = file_name.split(".")
    joined_path = "/".join(path)
    return f"{joined_path}_{number}.{extension}"


def list_file_shards(file_path, shard_length):

    *path, file_name = file_path.split("/")
    joined_path = "/".join(path)
    name, extension = file_name.split(".")
    shard = name[(shard_length) * -1 :]  # get shard number
    unsharded_name = name.replace(shard, "")  # get name without shard
    file_pattern = f"{joined_path}/{unsharded_name}*.{extension}"
    logging.info(f"The shard pattern is {file_pattern}")

    return glob.glob(file_pattern)


def get_first_folder(file_name):
    return file_name.split("/")[0]


def remove_first_folder(file_name):
    return "/".join(file_name.split("/")[1:])


def get_credentials(credentials, scopes=None, admin_user=None):
    if not credentials:
        return
    try:
        service_account_info = json.loads(credentials)
    except:
        with open(credentials, "r") as f:
            service_account_info = json.loads(f.read())

    credentials = service_account.Credentials.from_service_account_info(
        service_account_info, scopes=scopes
    )

    if admin_user:  # for GCP Directory API
        return credentials.with_subject(admin_user)

    return credentials


def timer(delay=5, delay_diff=2):
    sleep_min = delay - delay_diff
    sleep_max = delay + delay_diff

    sleep(random.uniform(sleep_min, sleep_max))


def edit_keys(dictionary, convert_function):
    """
    Edits the keys in a python dictionary
    """
    if isinstance(dictionary, (str, int, float)):
        return dictionary
    if isinstance(dictionary, dict):
        new = dictionary.__class__()
        for k, v in dictionary.items():
            new[convert_function(k)] = edit_keys(v, convert_function)
    elif isinstance(dictionary, (list, set, tuple)):
        new = dictionary.__class__(edit_keys(v, convert_function) for v in dictionary)
    else:
        return dictionary
    return new
