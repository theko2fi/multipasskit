from celery.app import Celery
import os
from ..sdk.multipass import MultipassClientSDK

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
app = Celery(__name__, broker=redis_url, backend=redis_url)

manager = MultipassClientSDK()

class AsyncMultipassVM():

    @staticmethod
    @app.task
    def start_task(name):
        return manager.get_vm(name).start()

class AsyncMultipassClient():
    """
    A derived class for async VM management using Celery.
    """

    @staticmethod
    @app.task
    def create_vm_task(vm_name: str, cpu: int, disk: str, mem: str, image, cloud_init):
        """
        A Celery task that wraps the instance method.
        """
        # Create an instance of the class and call the instance method
        return manager.launch(vm_name, cpu, disk, mem)