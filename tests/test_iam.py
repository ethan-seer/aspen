import os
import pytest
import shutil
from pprint import pprint as p

from google.oauth2 import service_account
from googleapiclient import discovery

from aspen.iam import CloudResourceManager
from aspen.iam import Recommender
from aspen.storage import Storage
from aspen.storage import Write
from aspen.storage import Read
from aspen.storage import Open
from aspen.request import APIClient as APIRequest

FILE_NAME = "iam/data.jsonl"
PARSED_FILE_NAME = "iam/data_parsed.jsonl"
FOLDERS, *_ = FILE_NAME.split("/")


@pytest.fixture
def credentials():
    yield os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")


# Cloud Resouce Manager


@pytest.fixture
def crm_request(credentials):
    yield APIRequest(
        provider="GoogleCloud", service="cloudresourcemanager", credentials=credentials
    )


@pytest.fixture
def crm():
    yield CloudResourceManager()


@pytest.mark.iam
@pytest.mark.cloudresourcemanager
@pytest.mark.cloudresourcemanager_fetch_without_storage
def test_cloudresourcemanager(crm, crm_request):

    projects = crm.fetch(request=crm_request, filter="parent.type:organization")
    assert len(projects) > 0


@pytest.mark.iam
@pytest.mark.cloudresourcemanager
@pytest.mark.cloudresourcemanager_fetch_with_storage
def test_cloudresourcemanager_with_storage(crm, crm_request):

    write_obj = Write(destination=FILE_NAME, method=Open, extension="jsonl", mode="w")

    write_storage = Storage(write_obj=write_obj)
    projects = crm.fetch(
        request=crm_request,
        write_storage=write_storage,
        filter="parent.type:organization",
    )

    assert os.path.exists(FILE_NAME) == True

    with open(FILE_NAME, "r") as f:
        data = f.read()
        assert len(data.split("\n")) > 0

    shutil.rmtree(FOLDERS)


# Recommender


@pytest.fixture
def r():
    yield Recommender()


@pytest.fixture
def r_request(credentials):
    yield APIRequest(
        provider="GoogleCloud", service="recommender", credentials=credentials
    )


RECOMMENDER_PROJECT_ID = os.environ.get("RECOMMENDER_PROJECT_ID")


@pytest.mark.iam
@pytest.mark.recommender
@pytest.mark.recommender_fetch_without_storage
def test_recommender_fetch_without_storage(r, r_request):
    if RECOMMENDER_PROJECT_ID:

        members = r.fetch(project_id=RECOMMENDER_PROJECT_ID)

        assert len(members) > 0
    else:
        print(
            "Please set RECOMMENDER_PROJECT_ID as an env variable to test 'recommender_fetch_without_storage'"
        )


@pytest.mark.iam
@pytest.mark.recommender
@pytest.mark.recommender_fetch_with_storage
def test_recommender_with_storage(r, r_request):

    if RECOMMENDER_PROJECT_ID:

        write_obj = Write(
            destination=FILE_NAME, method=Open, extension="jsonl", mode="w"
        )

        write_storage = Storage(write_obj=write_obj)
        members = r.fetch(
            project_id=RECOMMENDER_PROJECT_ID,
            write_storage=write_storage,
        )

        assert os.path.exists(FILE_NAME) == True

        with open(FILE_NAME, "r") as f:
            data = f.read()
            assert len(data.split("\n")) > 0

        shutil.rmtree(FOLDERS)
    else:
        print(
            "Please set RECOMMENDER_PROJECT_ID as an env variable to test 'recommender_fetch_with_storage'"
        )


@pytest.mark.iam
@pytest.mark.recommender
@pytest.mark.recommender_parse
def test_recommender_parse(r, r_request):

    if RECOMMENDER_PROJECT_ID:

        write_obj = Write(
            destination=FILE_NAME, method=Open, extension="jsonl", mode="w"
        )

        write_storage = Storage(write_obj=write_obj)
        members = r.fetch(
            project_id=RECOMMENDER_PROJECT_ID,
            write_storage=write_storage,
        )

        # read the written file
        read_obj = Read(destination=FILE_NAME, method=Open, extension="jsonl", mode="r")

        read_storage = Storage(read_obj=read_obj)

        write_obj = Write(
            destination=PARSED_FILE_NAME, method=Open, extension="jsonl", mode="w"
        )

        write_storage = Storage(write_obj=write_obj)
        r.parse(read_storage=read_storage, write_storage=write_storage)

        assert os.path.exists(FILE_NAME) == True
        assert os.path.exists(PARSED_FILE_NAME) == True

        with open(FILE_NAME, "r") as f:
            data = f.read()
            assert len(data.split("\n")) > 0

        with open(PARSED_FILE_NAME, "r") as f:
            data = f.read()
            assert len(data.split("\n")) > 0

        shutil.rmtree(FOLDERS)

    else:
        print(
            "Please set RECOMMENDER_PROJECT_ID as an env variable to test 'recommender_parse'"
        )
