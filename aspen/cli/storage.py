import os
import sys
import argparse
import logging
from pprint import pprint as p

from aspen.storage import Storage
from aspen.storage import Read
from aspen.storage import Write

WRITE_FORMATS = Storage.WRITE_FORMATS.keys()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Read and write data to storage.")
    parser.add_argument(
        "--action",
        "-a",
        type=str,
        nargs=1,
        choices=["read", "write"],
        help="Choose from read or write",
    )

    parser.add_argument(
        "--file-name",
        "-fn",
        type=str,
        nargs=1,
        help="Where the file can be located",
    )

    parser.add_argument(
        "--method",
        "-m",
        type=str,
        nargs=1,
        choices=["open"],
        help="Open is the only choice at this time.",
    )

    parser.add_argument(
        "--format",
        "-f",
        type=str,
        choices=WRITE_FORMATS,
        nargs=1,
        help="Where the file can be located",
    )

    args = parser.parse_args()

    action, file_name, method, format = (
        args.action,
        args.file_name[0],
        args.method[0],
        args.extension[0],
    )

    if "read" in action:
        if method == "open":
            method = open
        else:
            method = open
            logging.warning("Only 'open' is supported")

        read_obj = Read(file_name=file_name, method=method, extension=format)
        read_storage = Storage(read_obj=read_obj)
        print(read_storage.read())
