import aiohttp
from dask_fly import FLY_API_HOSTNAME, HEADERS
from dask_fly.utils import random_string

class FlyDaskScheduler:
    def __init__(self, app_name, region):
        self.app_name = app_name
        self.region = region
        self.name = f"dask-scheduler-{random_string()}"

    async def create(self):
        payload = {
            "name": self.name,
            "config": {
                "image": "daskdev/dask",
                "env": {
                    "EXTRA_PIP_PACKAGES": "dask[distributed]",
                    "DASK_SCHEDULER": "true",
                },
            },
            "region": self.region,
        }

        url = f"http://{FLY_API_HOSTNAME}/v1/apps/{self.app_name}/machines"
        async with aiohttp.ClientSession(headers=HEADERS) as session:
            async with session.post(url, json=payload) as response:
                if response.status == 200:
                    self.machine_id = (await response.json())["id"]
                    return self.machine_id
                else:
                    raise Exception(f"Error creating scheduler: {await response.text()}")

    async def delete(self):
        url = f"http://{FLY_API_HOSTNAME}/v1/apps/{self.app_name}/machines/{self.machine_id}"
        async with aiohttp.ClientSession(headers=HEADERS) as session:
            async with session.delete(url) as response:
                if response.status != 200:
                    raise Exception(f"Error deleting scheduler: {await response.text()}")
