from aspen.storage.storage import Storage
from aspen.storage.storage import Read
from aspen.storage.storage import Write

from aspen.storage.methods import Open
from aspen.storage.methods import GoogleCloudStorage
from aspen.storage.methods import GoogleBigQuery


option_values = {
    "open": Open,
    "google_cloud_storage": GoogleCloudStorage,
    "google_bigquery": GoogleBigQuery,
}


def options(method):

    try:
        return option_values[method]
    except KeyError:
        raise ValueError("You must use 'open' or 'google_cloud_storage'.")
