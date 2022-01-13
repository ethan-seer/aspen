from aspen.request import APIClient
from pprint import pprint as p


class Directory:
    def __init__(self, admin_user, credentials=None):
        self.credentials = credentials
        self.request = APIClient(
            provider="GoogleCloud",
            service="admin",
            credentials=self.credentials,
            scopes=["https://www.googleapis.com/auth/admin.directory.group.readonly"],
            admin_user=admin_user,
        )

    def list_groups(
        self,
    ):
        token = None
        groups = []

        while True:

            group_page = (
                self.request.client.groups()
                .list(customer="my_customer", pageToken=token)
                .execute()
            )
            token = group_page.get("nextPageToken")

            groups.extend(group_page["groups"])

            if not token:
                break

        return groups

    def get_group(self, group_key):
        try:
            return self.request.client.groups().get(groupKey=group_key).execute()
        except:
            return

    def _get_members(self, group_key):

        token = None
        members = []

        while True:

            try:
                member_page = (
                    self.request.client.members()
                    .list(groupKey=group_key, pageToken=token)
                    .execute()
                )
                token = member_page.get("nextPageToken")

                members.extend(member_page["members"])
            except:  # if no members exist
                return
            if not token:
                break

        return members

    def update_group(self, group_key, emails=[]):
        pass
