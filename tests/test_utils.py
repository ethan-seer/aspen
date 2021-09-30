import os
import shutil
import re

import pytest
from google.oauth2.service_account import Credentials

from aspen.utils import create_shard
from aspen.utils import create_folder
from aspen.utils import list_file_shards
from aspen.utils import get_credentials
from aspen.utils import edit_keys


@pytest.mark.utils
@pytest.mark.utils_create_shard
def test_create_shard():
    file_name = "my/best/folder/data.json"
    results = create_shard(file_name=file_name, number="0001")
    expected = "my/best/folder/data_0001.json"
    assert expected == results


@pytest.mark.utils
@pytest.mark.utils_create_folder
def test_utils_create_folder():
    file_name = "a/b/c.json"
    create_folder(file_name=file_name)
    assert os.path.exists("a/b")
    shutil.rmtree("a")


@pytest.mark.utils
@pytest.mark.utils_list_file_shards
def test_utils_list_file_shards():
    file_name = "a/b/c_0000000000.json"
    create_folder(file_name=file_name)
    open("a/b/c_0000000001.json", "w")
    open("a/b/c_0000000002.json", "w")
    open("a/b/c_0000000003.json", "w")
    open("a/b/c_0000000004.json", "w")
    open("a/b/c_0000000005.json", "w")
    open("a/b/nonsense.json", "w")

    results = list_file_shards(file_path=file_name, shard_length=10)
    assert len(results) == 5
    shutil.rmtree("a")


SERVICE_ACCOUNT = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")


@pytest.mark.utils
@pytest.mark.utils_get_credentials
def test_utils_get_credentials():
    credentials = get_credentials(credentials=SERVICE_ACCOUNT)
    assert isinstance(credentials, Credentials)


TEST_DICT = {"a-b": {"a.c": "d"}}
EXPECTED_DICT = {"_a_b": {"_a_c": "d"}}


def convert_function(string):
    no_punc_string = re.sub(r"\-|\.", "_", string)
    return "_" + no_punc_string


@pytest.mark.utils
@pytest.mark.utils_edit_keys
def test_utils_edit_keys():

    convert = convert_function
    results = edit_keys(dictionary=TEST_DICT, convert_function=convert_function)
    assert EXPECTED_DICT == results
