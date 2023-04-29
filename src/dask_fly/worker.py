import aiohttp
from dask_fly import FLY_API_HOSTNAME, HEADERS, EXTRA_PIP_PACKAGES
from dask_fly.utils import random_string

class FlyDaskWorker:
    def __init__(self, app_name, region, name=None, memory=None, cpu=None):
        self.app_name = app_name
        self.region = region
        self.name = name or f"worker-{region}-{random_string()}"
        self.memory = memory
        self.cpu = cpu

    async def create(self):
        payload = {
            "name": self.name,
            "config": {
                "image": "daskdev/dask",
                "env": {
                    "EXTRA_PIP_PACKAGES": EXTRA_PIP_PACKAGES,
                },
            },
            "region": self.region,
        }

        if self.memory is not None:
            payload["config"]["memory"] = self.memory
        if self.cpu is not None:
            payload["config"]["cpu"] = self.cpu

        url = f"https://{FLY_API_HOSTNAME}/v1/apps/{self.app_name}/machines"
        async with aiohttp.ClientSession(headers=HEADERS) as session:
            async with session.post(url, json=payload) as response:
                if response.status == 200:
                    self.machine_id = (await response.json())["id"]
                    return self.machine_id
                else:
                    raise Exception(f"Error creating worker: {await response.text()}")

    async def delete(self):
        url = f"https://{FLY_API_HOSTNAME}/v1/apps/{self.app_name}/machines/{self.machine_id}"
        async with aiohttp.ClientSession(headers=HEADERS) as session:
            async with session.delete(url) as response:
                if response.status != 200:
                    raise Exception(f"Error deleting worker: {await response.text()}")
