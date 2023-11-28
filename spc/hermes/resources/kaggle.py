import requests
import requests.auth
from dagster import ConfigurableResource


class KaggleResource(ConfigurableResource):
    """Resource used to connect to Kaggle"""

    username: str
    password: str

    def download_request(self, owner: str, dataset: str) -> bytes:
        source = f"https://www.kaggle.com/api/v1/datasets/download/{owner}/{dataset}"
        auth = requests.auth.HTTPBasicAuth(self.username, self.password)
        response = requests.get(source, stream=True, timeout=300, auth=auth)

        if response.status_code != 200:
            raise RuntimeError("Response code is not 200.")

        if response.headers["Content-Type"] != "application/zip":
            raise RuntimeError("Response is not a zip file.")

        return response.content
