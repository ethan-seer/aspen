import os
import pytest
import shutil
from pprint import pprint as p

from google.oauth2 import service_account


from aspen.directory import Directory
from aspen.storage import Storage
from aspen.storage import Write
from aspen.storage import Read
from aspen.storage import Open
from aspen.request import APIClient as APIRequest


@pytest.fixture
def directory_client():
    credentials = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    admin_user = os.environ["ADMIN_USER"]
    return Directory(credentials=credentials, admin_user=admin_user)


@pytest.mark.directory
@pytest.mark.directory_list_groups
def test_directory_list_groups(directory_client):

    groups = directory_client.list_groups()
    p(groups)
    assert len(groups) > 0


@pytest.mark.directory
@pytest.mark.directory_get_group
@pytest.mark.directory_get_group_valid
def test_directory_get_group_valid(directory_client):

    group_key = os.environ["TEST_GROUP_KEY"]
    group = directory_client.get_group(group_key=group_key)

    assert len(group) > 0


@pytest.mark.directory
@pytest.mark.directory_get_group
@pytest.mark.directory_get_group_invalid
def test_directory_get_group_invalid(directory_client):

    group = directory_client.get_group(group_key="abc")

    assert group == None


@pytest.mark.directory
@pytest.mark.directory_get_members
@pytest.mark.directory_get_members_valid
def test_directory_get_members_valid(directory_client):

    group_key = os.environ["TEST_GROUP_KEY"]

    members = directory_client._get_members(group_key=group_key)
    

    assert len(members) > 0


@pytest.mark.directory
@pytest.mark.directory_get_members
@pytest.mark.directory_get_members_invalid
def test_directory_get_members_invalid(directory_client):

    group = directory_client._get_members(group_key="abc")

    assert group == None


@pytest.mark.directory
@pytest.mark.directory_update_group
def test_directory_update_group(directory_client):

    group = directory_client.update_group(group_key="abc")

    p(group)
