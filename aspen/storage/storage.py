import json
import logging
from collections import namedtuple
import csv

import pandas as pd
from pandas.core.frame import DataFrame

from aspen.storage.methods import Open
from aspen.storage.methods import GoogleCloudStorage


class Storage:

    WRITE_FORMATS = {
        "jsonl": lambda x: "\n".join([json.dumps(y) for y in x]),
        "list": lambda x: " ".join([str(y) for y in x]),
        "dict": lambda x: json.dumps(x),
        "str": lambda x: x,
        "csv": lambda x: Storage._convert_to_csv(x),
        "png": lambda x: x,
    }

    READ_FORMATS = {
        "jsonl": lambda x: [json.loads(x) for x in x.split("\n")],
        "json": lambda x: json.loads(x),
        "str": lambda x: x,
        "pandas": lambda x: pd.read_csv(x),
    }

    def __init__(self, read_obj=None, write_obj=None):
        self.read_obj = read_obj
        self.write_obj = write_obj

    @classmethod
    def _convert_to_csv(self, data):
        """data must be a list of dicts"""
        first_row, *_ = data
        header = first_row.keys()

        # start with the header
        csv_data = [",".join(header)]

        for row in data:
            wrong_fields = row.keys() - header
            if wrong_fields:
                raise ValueError(
                    "dict contains fields not in fieldnames: "
                    + ", ".join([repr(x) for x in wrong_fields])
                )
            row_data = list()
            for key in header:

                cell_data = str(row.get(key, '""'))
                if "," in cell_data:
                    cell_data = f'"{cell_data}"'
                row_data.append(cell_data)

            csv_data.append(",".join(row_data))

        return "\n".join(csv_data)

    def _format_data(self, data):

        # if the format is known
        if self.write_obj.extension in Storage.WRITE_FORMATS.keys():
            return Storage.WRITE_FORMATS[self.write_obj.extension](data)
        # if the format is unknown
        else:

            if not isinstance(data, (list, tuple, dict, str, data)):
                logging.info("Unknown data format. Must be a list, tuple, dict or str.")
            if isinstance(data, (list, tuple)):
                logging.info("Converting list or tuple data to str.")
                sample, *_ = data
                if isinstance(sample, dict):
                    format_data = Storage.WRITE_FORMATS["jsonl"]
                else:
                    format_data = Storage.WRITE_FORMATS["list"]
            if isinstance(data, dict):
                logging.info("Converting dict data to json.")
                format_data = Storage.WRITE_FORMATS["dict"]
            if isinstance(data, str):
                logging.info("Not converting data because it's already a str.")
                format_data = Storage.WRITE_FORMATS["str"]
            if isinstance(data, DataFrame):
                return data

            return format_data(data)

    def write(self, data):
        """jsonl needs to be a list. if a list is passed in it will be joined with a space"""
        formatted_data = self._format_data(data)

        self.write_obj.method(
            destination=self.write_obj.destination,
            extension=self.write_obj.extension,
            service_account=self.write_obj.service_account,
        ).write(data=formatted_data)

        return formatted_data

    def read(
        self,
    ):

        data = self.read_obj.method(
            destination=self.read_obj.destination,
            extension=self.read_obj.extension,
            service_account=self.read_obj.service_account,
        ).read()
        if data:
            return Storage.READ_FORMATS[self.read_obj.extension](data)


def format_validator(instance, attribute, value):
    # TODO: create format validator
    pass


class Read:
    def __init__(
        self, destination, mode=None, method=Open, extension=None, service_account=None
    ):
        self.destination = destination
        self.mode = mode
        self.method = method
        self.extension = extension
        self.service_account = service_account


class Write:
    def __init__(
        self, destination, mode=None, method=Open, extension=None, service_account=None
    ):
        self.destination = destination
        self.mode = mode
        self.method = method
        self.extension = extension
        self.service_account = service_account
