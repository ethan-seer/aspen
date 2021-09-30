import os

import pytest
from google.oauth2 import service_account
from googleapiclient.discovery import Resource

from aspen.request import APIClient


@pytest.fixture
def credentials():
    yield os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")


@pytest.mark.request
@pytest.mark.request_google_cloud
@pytest.mark.request_google_cloud_cloud_resource_manager
def test_equest_google_cloud_cloud_resource_manager(credentials):

    crm = APIClient(
        provider="GoogleCloud", service="cloudresourcemanager", credentials=credentials
    )

    assert isinstance(crm.client, Resource)


@pytest.mark.request
@pytest.mark.request_google_cloud
@pytest.mark.request_google_cloud_cloud_recommender
def test_request_google_cloud_cloud_recommender(credentials):

    crm = APIClient(
        provider="GoogleCloud", service="recommender", credentials=credentials
    )

    assert isinstance(crm.client, Resource)
