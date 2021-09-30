import os
import sys
import argparse
import logging
from pprint import pprint as p

from google.oauth2 import service_account

sys.path.append("..")

from aspen.iam import CloudResourceManager
from aspen.iam import Recommender
from aspen.storage import Storage
from aspen.storage import Write
from aspen.storage import Read
from aspen.request import APIClient
from aspen.storage import options

WRITE_FORMATS = Storage.WRITE_FORMATS.keys()


def main():
    parser = argparse.ArgumentParser(description="Get IAM data.")

    parser.add_argument(
        "--source",
        "-s",
        type=str,
        nargs=1,
        choices=["cloudresourcemanager", "recommender"],
        help="Choose from fetch, clean or analyze",
    )
    parser.add_argument(
        "--action",
        "-a",
        type=str,
        nargs="+",
        choices=["fetch", "parse", "analyze"],
        help="Choose from fetch, clean or analyze",
    )

    parser.add_argument(
        "--credentials",
        "-c",
        type=str,
        nargs=1,
        help="You must identify where credentials are coming from",
    )

    parser.add_argument(
        "--read-file",
        "-rf",
        type=str,
        nargs=3,
        default=[
            "open",
            "jsonl",
            "data/iam/raw/projects.jsonl",
        ],
        help="You must identify the file method, format and name. open and google_cloud_storage are method options",
    )

    parser.add_argument(
        "--write-file",
        "-wf",
        type=str,
        nargs=3,
        default=[
            "open",
            "jsonl",
            "data/iam/raw/projects.jsonl",
        ],
        help="You must identify the file method, format and name. open and google_cloud_storage are method options",
    )

    parser.add_argument(
        "--project-id",
        "-pid",
        type=str,
        nargs=1,
        help="When using Recommender, you must specify a project ID.",
    )

    args = parser.parse_args()

    source, action, credentials, write_file, read_file, project_id = (
        args.source[0],
        args.action[0],
        args.credentials[0] if args.credentials else None,
        args.write_file,
        args.read_file,
        args.project_id[0] if args.project_id else None,
    )

    write_file_method, write_file_format, write_file_name = write_file
    read_file_method, read_file_format, read_file_name = read_file

    write_method_option = options(method=write_file_method)
    read_method_option = options(method=read_file_method)

    # # prepare requests

    crm_request = APIClient(
        provider="GoogleCloud", service="cloudresourcemanager", credentials=credentials
    )
    r_request = APIClient(
        provider="GoogleCloud", service="recommender", credentials=credentials
    )

    # prepare write storage
    if write_file:

        write_obj = Write(
            destination=write_file_name,
            method=write_method_option,
            extension="jsonl",
            service_account=credentials,
        )

        write_storage = Storage(write_obj=write_obj)

    else:
        write_storage = None

    # prepare write storage
    if read_file:

        read_obj = Read(
            destination=read_file_name,
            method=read_method_option,
            extension="jsonl",
            service_account=credentials,
        )

        read_storage = Storage(read_obj=read_obj)

    else:
        read_storage = None

    if "cloudresourcemanager" in source:

        if "fetch" in action:

            crm = CloudResourceManager()

            projects = crm.fetch(
                request=crm_request,
                write_storage=write_storage,
                filter="parent.type:organization",
            )

    if "recommender" in source:

        if "fetch" in action:

            r = Recommender()
            members = r.fetch(
                request=r_request, project_id=project_id, write_storage=write_storage
            )

        if "parse" in action:

            r = Recommender()
            r.parse(write_storage=write_storage, read_storage=read_storage)


if __name__ == "__main__":
    main()
