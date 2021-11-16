from aspen.request import APIClient


class Directory:
    def __init__(self, credentials=None):
        self.credentials = credentials
        self.request = APIClient(
            provider="GoogleCloud", service="admin", credentials=self.credentials
        )

    def get_group(self, group_name):

        results = (
            self.request.client.groups()
            .list(
                domain="seerinteractive.com",
                customer="my_customer",
                maxResults=10,
                orderBy="email",
            )
            .execute()
        )
        print(results)
        # users = results.get("users", [])
