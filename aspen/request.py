import logging
import os

from googleapiclient import discovery

from aspen.utils import get_credentials
from aspen.utils import timer


class APIClient:

    """Container for all API clients, i.e. not Cloud Functions, Request"""

    SERVICES = {
        "GoogleCloud": {
            "cloudresourcemanager": discovery.build,
            "recommender": discovery.build,
            "storage": discovery.build,
            "admin": discovery.build,
        }
    }

    def __init__(self, provider, service, credentials=None):
        self.provider = provider
        self.service = service
        self.credentials = get_credentials(credentials=credentials)
        self.client = None

        self.version = "directory_v1" if self.service == "admin" else "v1"

        if self.provider == "GoogleCloud":

            self.client = APIClient.SERVICES[self.provider][self.service](
                self.service, self.version, credentials=self.credentials
            )
