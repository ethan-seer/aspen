import logging
import os
from collections import namedtuple


from aspen.storage import Storage
from aspen.request import APIClient

Project = namedtuple(
    "Project",
    [
        "number",
        "id",
        "lifecycle_state",
        "name",
        "create_time",
        "parent",
    ],
)


class CloudResourceManager:
    """Uses Google's Cloud Resource Manager"""

    def __init__(self, credentials=None):
        self.credentials = credentials
        self.request = APIClient(
            provider="GoogleCloud",
            service="cloudresourcemanager",
            credentials=self.credentials,
        )

    def fetch(self, write_storage=None, **options):

        """returns a series of projects"""
        token = None
        page_count = 0
        filter = options.get("filter")

        projects = list()

        while True:

            request = self.request.client.projects().list(
                pageToken=token, filter=filter
            )
            response = request.execute()

            for project in response.get("projects", []):

                number = project["projectNumber"]
                id = project["projectId"]
                lifecycle_state = project["lifecycleState"]
                name = project["name"]
                create_time = project["createTime"]
                parent = project["parent"]

                logging.info(f"Getting project: {name}")

                project = Project(
                    number=number,
                    id=id,
                    lifecycle_state=lifecycle_state,
                    name=name,
                    create_time=create_time,
                    parent=parent,
                )

                projects.append(project)

            page_count += 1

            logging.info(
                f"Resource page count {page_count}. Current project count: {len(projects)}"
            )
            try:
                token = response["nextPageToken"]
            except KeyError:
                break

        # write to storage object
        if write_storage:
            logging.info(f"Writing data to file {write_storage.write_obj.destination}")
            data = [project._asdict() for project in projects]
            write_storage.write(data=data)

        return projects

    def parse(
        self,
        read_storage,
        write_storage=None,
    ):
        raise NotImplementedError

    def analyze(
        self,
        read_storage,
        write_storage=None,
    ):
        raise NotImplementedError


def recursive_items(dictionary):
    for key, value in dictionary.items():
        if type(value) is dict:
            yield from recursive_items(value)
        else:
            yield (key, value)


class Recommender:
    """HI"""

    def __init__(self, credentials=None):
        self.credentials = credentials
        self.request = APIClient(
            provider="GoogleCloud", service="recommender", credentials=self.credentials
        )

    def fetch(self, project_id, parent=None, write_storage=None):

        parent = f"projects/{project_id}/locations/global/insightTypes/google.iam.policy.Insight"
        insights = (
            self.request.client.projects()
            .locations()
            .insightTypes()
            .insights()
            .list(parent=parent)
            .execute()
        )

        try:
            recommendations = insights["insights"]
        except KeyError:
            logging.info(f"Could not get insights for {project_id}")
            return []

        members = {}

        for recommendation in recommendations:
            email_type, email = recommendation["content"]["member"].split(":")

            members.setdefault(email, {})
            role = (
                recommendation["content"]["role"]
                .replace(".", "_")
                .replace("/", "_")
                .replace("-", "_")
            )  # for bigquery
            members[email][role] = recommendation

        member_list = list()

        for email, user_data in members.items():
            data = {"email": email}
            data.update(user_data)  # update all member data to record

            member_list.append(data)

        # write to storage object
        if write_storage:
            write_storage.write(member_list)

        return member_list

    def parse(
        self,
        read_storage,
        write_storage=None,
    ):
        members = read_storage.read() or []  # if the file doesn't exist

        clean_members = []

        for member in members:
            for role, user_data in member.items():
                if isinstance(user_data, dict):
                    user_data.update({"role": role})
                    user_data.update({"email": member.get("email")})

                    clean_members.append(user_data)

        if write_storage:
            write_storage.write(clean_members)

        return clean_members

    def analyze(
        self,
        read_storage,
        write_storage=None,
    ):
        raise NotImplementedError
