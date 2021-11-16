import os
import pytest
import shutil
from pprint import pprint as p

from google.oauth2 import service_account
from googleapiclient import discovery

from aspen.directory import Directory
from aspen.storage import Storage
from aspen.storage import Write
from aspen.storage import Read
from aspen.storage import Open
from aspen.request import APIClient as APIRequest


@pytest.mark.directory
@pytest.mark.directory_get_group
def test_directory_get_group():
    directory = Directory()
    directory.get_group(group_name= 'abc')
