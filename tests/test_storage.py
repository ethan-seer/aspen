import os
import shutil

import pytest

from aspen.storage import Storage
from aspen.storage import Read
from aspen.storage import Write
from aspen.storage.methods import Open

EXPECTED_DATA_JSONL = """{"a": "b"}\n{"c": "d"}"""
EXPECTED_DATA_NOFORMAT = """{'a': 'b'} {'c': 'd'}"""
EXPECTED_DATA_COMPLEX_TXT = 'a,b\n"a , b",2.2\n2,3'

TEST_DATA_TXT = [{"a": "b"}, {"c": "d"}]

TEST_DATA_COMPLEX_TXT = [{"a": "a , b", "b": 2.2}, {"a": 2, "b": 3}]
FILE_NAME_TXT = "test_data/YYYY/MM/DD/test_file.txt"

FILE_NAME_CSV = "test_data/YYYY/MM/DD/test_file.csv"
TEST_DATA_CSV = [{"a": "b"}, {"a": "c"}]
FOLDERS, *_ = FILE_NAME_TXT.split("/")


@pytest.mark.storage
@pytest.mark.storage_write
@pytest.mark.storage_write_with_format_jsonl
def test_storage_write_with_format_jsonl():

    write = Write(destination=FILE_NAME_TXT, method=Open, extension="jsonl", mode="w")

    storage = Storage(write_obj=write)
    storage.write(data=TEST_DATA_TXT)

    assert os.path.exists(FILE_NAME_TXT) == True

    with open(FILE_NAME_TXT, "r") as f:
        saved_data = f.read()
        assert saved_data == EXPECTED_DATA_JSONL

    shutil.rmtree(FOLDERS)


@pytest.mark.storage
@pytest.mark.storage_write
@pytest.mark.storage_write_with_format_csv
def test_storage_write_with_format_csv():

    write = Write(destination=FILE_NAME_CSV, method=Open, extension="csv", mode="w")

    storage = Storage(write_obj=write)
    storage.write(data=TEST_DATA_CSV)

    assert os.path.exists(FILE_NAME_CSV) == True

    shutil.rmtree(FOLDERS)


@pytest.mark.storage
@pytest.mark.storage_format_write_data
def test_storage_format_write_data():
    write_obj = Write(
        destination=FILE_NAME_TXT,
        method=Open,
    )

    storage = Storage(write_obj=write_obj)
    assert storage._format_write_data(TEST_DATA_TXT) == EXPECTED_DATA_JSONL


@pytest.mark.storage
@pytest.mark.storage_write
@pytest.mark.storage_write_without_format
def test_storage_write_without_format():

    write_obj = Write(
        destination=FILE_NAME_TXT,
        method=Open,
    )

    storage = Storage(write_obj=write_obj)
    storage.write(
        data=TEST_DATA_TXT,
    )

    with open(FILE_NAME_TXT, "r") as f:
        saved_data = f.read()
        assert saved_data == EXPECTED_DATA_JSONL

    shutil.rmtree(FOLDERS)


@pytest.mark.storage
@pytest.mark.storage_read
def test_storage_read():
    write_obj = Write(destination=FILE_NAME_TXT, method=Open, extension="jsonl")
    read_obj = Write(destination=FILE_NAME_TXT, method=Open, extension="jsonl")

    storage = Storage(write_obj=write_obj, read_obj=read_obj)
    storage.write(data=TEST_DATA_TXT)

    result = storage.read()

    assert result == [{"a": "b"}, {"c": "d"}]

    shutil.rmtree(FOLDERS)


@pytest.mark.storage
@pytest.mark.storage_write
@pytest.mark.storage_format_data_jsonl
def test_storage_format_data_jsonl():

    write_obj = Write(destination=FILE_NAME_TXT, method=Open, extension="jsonl")
    storage = Storage(write_obj=write_obj)

    assert storage._format_write_data(TEST_DATA_TXT) == EXPECTED_DATA_JSONL


@pytest.mark.storage
@pytest.mark.storage_write
@pytest.mark.storage_convert_to_csv
def test_storage_convert_to_csv():

    write_obj = Write(destination=FILE_NAME_TXT, method=Open, extension="csv")
    storage = Storage(write_obj=write_obj)
    result = storage._convert_to_csv(TEST_DATA_COMPLEX_TXT)
    assert result == EXPECTED_DATA_COMPLEX_TXT
