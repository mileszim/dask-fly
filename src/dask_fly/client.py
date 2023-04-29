import asyncio
from dask.distributed import Client
from distributed.deploy.cluster import Cluster
from dask_fly.scheduler import FlyDaskScheduler
from dask_fly.worker import FlyDaskWorker

class FlyDaskClient(Client):
    def __init__(self, app_name, cluster, *args, **kwargs):
        self.app_name = app_name
        self.cluster = cluster
        # We need to initialize the Client instance first
        super().__init__("", *args, **kwargs)
        self.loop.run_until_complete(cluster.ensure_scheduler())
        self.set_as_default()
        self.scheduler_address = cluster.scheduler_address  # Update the scheduler address

    async def add_worker(self, region, name=None, memory=None, cpu=None):
        worker = FlyDaskWorker(self.app_name, region, name, memory, cpu)
        await worker.create()
        self.cluster.workers.append(worker)

    async def remove_worker(self, worker):
        await worker.delete()
        self.cluster.workers.remove(worker)


class FlyDaskCluster(Cluster):
    def __init__(self, app_name, scheduler_region, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app_name = app_name
        self.scheduler = FlyDaskScheduler(app_name, scheduler_region)
        self.scheduler.create()
        self.workers = []

    def __del__(self):
        for worker in self.workers:
            worker.delete()
        self.scheduler.delete()

    async def ensure_scheduler(self):
        while self.scheduler_address is None or self.scheduler_address == "<Not Connected>":
            await asyncio.sleep(1)
