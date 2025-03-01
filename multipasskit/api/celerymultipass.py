from celery.app import Celery
from multipasskit.sdk.multipass import MultipassClientSDK
from multipasskit.api.config import settings

celery_app = Celery(
    "multipasskit",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    imports=["multipasskit.sdk.multipass"],
    )


manager = MultipassClientSDK()

class AsyncMultipassVM():

    @celery_app.task
    def start_task(name):
        return manager.get_vm(name).start()
    
    @celery_app.task
    def stop_task(name):
        return manager.get_vm(name).stop()
    
    @celery_app.task
    def restart_task(name):
        return manager.get_vm(name).restart()
    

class AsyncMultipassClient():
    """
    A derived class for async VM management using Celery.
    """

    @staticmethod
    @celery_app.task
    def launch_task(vm_name: str, cpu: int, disk: str, mem: str, image, cloud_init):
        """
        A Celery task that wraps the instance method.
        """
        return manager.launch(**locals())
