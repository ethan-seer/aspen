import os
from numpy.random import randint

import pytest
from google.cloud.storage.bucket import Bucket
from google.cloud.storage.blob import Blob

from aspen.storage.methods import GoogleCloudStorage
from aspen.storage.methods import GoogleBigQuery

TEST_DATA_STR = """HI THERE"""

GENERIC_BUCKET_NAME = "google"
random_number = randint(0, 100000)
UNIQUE_BUCKET_NAME = f"unique-bucket-{random_number}"

SERVICE_ACCOUNT = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

TXT_FILE_PATH = "{bucket_name}/my/data.txt"


@pytest.fixture
def generic_write_obj():
    destination = TXT_FILE_PATH.format(bucket_name=GENERIC_BUCKET_NAME)
    yield GoogleCloudStorage(destination=destination, service_account=SERVICE_ACCOUNT)


@pytest.fixture
def unique_write_obj():
    destination = TXT_FILE_PATH.format(bucket_name=UNIQUE_BUCKET_NAME)
    yield GoogleCloudStorage(destination=destination, service_account=SERVICE_ACCOUNT)


@pytest.fixture
def unique_read_obj():
    destination = TXT_FILE_PATH.format(bucket_name=UNIQUE_BUCKET_NAME)
    yield GoogleCloudStorage(destination=destination, service_account=SERVICE_ACCOUNT)


@pytest.mark.methods
@pytest.mark.google_cloud_get_or_create_bucket_generic
def test_google_cloud_get_or_create_bucket_generic(generic_write_obj):
    with pytest.raises(ValueError):
        generic_write_obj._get_or_create_bucket()


@pytest.mark.methods
@pytest.mark.google_cloud_get_or_create_bucket_unique
def test_google_cloud_get_or_create_bucket_unique(unique_write_obj):
    bucket = unique_write_obj._get_or_create_bucket()
    assert isinstance(bucket, Bucket)


@pytest.mark.methods
@pytest.mark.google_cloud_write
def test_google_cloud_write(unique_write_obj):

    blob = unique_write_obj.write(data=TEST_DATA_STR)

    assert isinstance(blob, Blob)
    assert blob.exists()
    # clean up

    blob.delete()

    bucket = blob.bucket
    bucket.delete()


@pytest.fixture
def write_data(unique_write_obj):
    yield unique_write_obj.write(data=TEST_DATA_STR)


@pytest.mark.methods
@pytest.mark.google_cloud_read
def test_google_cloud_read(write_data, unique_read_obj):

    result = unique_read_obj.read()
    assert result == TEST_DATA_STR


@pytest.mark.methods
@pytest.mark.bigquery_read
def test_bigquery_read():
    query = """
        SELECT name, SUM(number) as total_people
        FROM `bigquery-public-data.usa_names.usa_1910_2013`
        WHERE state = 'TX'
        GROUP BY name, state
        ORDER BY total_people DESC
        LIMIT 20
    """
    result = GoogleBigQuery(destination=query, service_account=SERVICE_ACCOUNT).read()

    assert len(result) > 0
    assert list(result[0].keys()) == ["name", "total_people"]
