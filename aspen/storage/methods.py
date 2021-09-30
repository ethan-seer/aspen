import sys
import csv
import json
import logging

import pandas as pd
from google.cloud import storage
from google.cloud.storage.blob import Blob

# exceptions
from google.api_core.exceptions import NotFound
from google.api_core.exceptions import BadRequest

from aspen.utils import get_first_folder
from aspen.utils import remove_first_folder
from aspen.utils import get_credentials
from aspen.utils import create_folder


class Open:
    def __init__(self, destination, extension, mode="w", service_account=None):
        self.destination = destination
        self.mode = mode
        self.extension = extension
        # creates folders for file path locally
        create_folder(self.destination)

    def write(self, data):
        """open is idempotent"""
        with open(self.destination, self.mode) as f:
            f.write(data)

    def read(self):
        with open(self.destination, "r") as f:
            data = f.read()
        return data


class Pandas:
    def __init__(self, destination, extension=None, mode=None, service_account=None):
        self.destination = destination

    def write(self, data):
        """open is idempotent"""
        if "csv" in self.destination:
            data.to_csv(self.destination)
        elif "png" in self.destination:
            plt.savefig(self.destination)
        else:
            pass

    def read(self):
        return pd.read_csv(self.destination)


class GoogleCloudStorage:
    """the service account must have
    storage.buckets.create
    storage.buckets.get
    storage.buckets.delete

    storage.objects.create
    storage.objects.delete

    """

    CONTENT_TYPE = {
        "csv": "text/csv",
        "json": "application/json",
        "png": "image/png",  # TODO
        "txt": "text/plain",
        "jsonl": "text/plain",
    }

    def __init__(
        self,
        destination,
        service_account,
        extension="txt",
        mode=None,
    ):
        self.destination = destination  # note: the bucket name is the first folder
        self.service_account = service_account  # can be json or file
        self.extension = extension
        self._credentials = get_credentials(credentials=service_account)
        self._client = storage.Client(credentials=self._credentials)  # GCS client

    def _get_or_create_bucket(
        self,
    ):
        """gets or creates a bucket based on the first folder in the destination path"""
        bucket_name = get_first_folder(self.destination)
        try:
            return self._client.get_bucket(bucket_name)
        except NotFound:
            try:
                return self._client.create_bucket(bucket_name)
            except BadRequest:
                raise ValueError(
                    f"{bucket_name} is already taken. Please choose another name."
                )

    def write(self, data):
        """write is idempotent and returns a blob"""

        bucket = self._get_or_create_bucket()
        name = remove_first_folder(file_name=self.destination)
        blob = Blob(name=name, bucket=bucket)

        content_type = GoogleCloudStorage.CONTENT_TYPE.get(self.extension, "txt")

        blob.upload_from_string(data=data, content_type=content_type)
        return blob

    def read(self):
        bucket = self._get_or_create_bucket()
        name = remove_first_folder(file_name=self.destination)
        blob = Blob(name=name, bucket=bucket)
        try:
            return blob.download_as_string().decode()
        except NotFound:
            logging.info(f"File is not found: {self.destination}")
            return
