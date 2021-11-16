import json
import os
import sys
import argparse
import logging
from pprint import pprint as p

from google.oauth2 import service_account

sys.path.append("..")

# clients
from aspen.iam import CloudResourceManager
from aspen.iam import Recommender
from aspen.directory import Directory
from aspen.storage_client import StorageClient

# storage
from aspen.storage import Storage
from aspen.storage import Write
from aspen.storage import Read
from aspen.storage import option_values

from aspen.request import APIClient

from aspen.cli.utils import build_source

modules = {}

for module in dir():
    first_letter, *_ = module
    if first_letter == "_":
        break
    else:
        modules.update({module.lower(): module})

available_classes = [*modules.keys()]


def main():

    parser = argparse.ArgumentParser(description="Get IAM data.")

    parser.add_argument(
        "--source",
        "-s",
        type=str,
        choices=available_classes,
        required=True,
        help=f"The class name.",
    )
    parser.add_argument(
        "--method",
        "-m",
        type=str,
        required=True,
    )

    parser.add_argument(
        "--params",
        "-p",
        type=str,
        required=False,
        default="{}",  # empty dict
        help="Any params used in the method (exclude read_storage and write_storage). Must be a json string",
    )
    parser.add_argument(
        "--global-credentials",
        "-gc",
        type=str,
        default=None,
        required=False,
        help="Default credentials that will be used if credentials are not attached to --read-source or --write-source",
    )

    parser.add_argument(
        "--read-source",
        "-rs",
        type=str,
        nargs="*",
        required=False,
        default=[None, None, None, None],
        help=f"""
                You must identify the source 
                method ({', '.join([*option_values])}), 
                format ({', '.join([*Storage.READ_FORMATS])}) and 
                name (destination name, which can be a file path or SQL), 
                e.g. open jsonl data/stuff.jsonl path/to/credentials.json
            """,
    )

    parser.add_argument(
        "--write-source",
        "-ws",
        type=str,
        nargs="*",
        required=False,
        default=[None, None, None, None],
        help=f"""
                You must identify the source 
                method ({', '.join([*option_values])}), 
                format ({', '.join([*Storage.WRITE_FORMATS])}) and 
                name (destination name, which can be a file path or SQL), 
                e.g. open jsonl data/stuff.jsonl path/to/credentials.json
            """,
    )

    args, unknown = parser.parse_known_args()

    source = args.source
    method = args.method
    credentials = args.global_credentials
    params = json.loads(args.params)  # get the first item in list

    write_source = args.write_source
    read_source = args.read_source

    read_obj = build_source(
        storage_type=Read, source=read_source, credentials=credentials
    )

    if read_obj:
        read_storage = Storage(read_obj=read_obj)
        params.update({"read_storage": read_storage})

    write_obj = build_source(
        storage_type=Write, source=write_source, credentials=credentials
    )

    if write_obj:
        write_storage = Storage(write_obj=write_obj)
        params.update({"write_storage": write_storage})

    class_instance = eval(modules[source])(credentials=credentials)

    method_instance = getattr(class_instance, method)

    method_instance(**params)


if __name__ == "__main__":
    main()
