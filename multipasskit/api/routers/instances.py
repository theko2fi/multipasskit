from fastapi import  APIRouter
from typing import Union
from multipasskit.api.models import instance, mount
from multipasskit.sdk.multipass import MultipassClientSDK
from multipasskit.api.celerymultipass import AsyncMultipassClient, AsyncMultipassVM

router = APIRouter(prefix='/instances', tags=["instances"])

async_multipass_client = AsyncMultipassClient()

@router.get("/")
def list_instances():
    return MultipassClientSDK().list()

@router.get("/{name}")
def instance_info(name: str):
    return MultipassClientSDK().get_vm(vm_name=name).info()

@router.post("/{name}/exec")
def exec_command(cmd: str, name: str):
    vm = MultipassClientSDK().get_vm(vm_name=name)
    stdout, stderr = vm.exec(cmd_to_execute=cmd)
    return {"result": stdout, "error": stderr}

@router.get("/{name}/snapshots")
def list_instance_snaphots(name: str):
    pass

@router.post("/{name}/recover")
def recover_instance(name: str):
    return MultipassClientSDK().recover(vm_name=name)

@router.delete("/{name}")
def delete_instance(name: str, purge: bool = False):
    return MultipassClientSDK().get_vm(vm_name=name).delete(purge=purge)

@router.post("/{name}/stop")
def stop_instance(name: str):
    return MultipassClientSDK().get_vm(vm_name=name).stop()
    #return vm.stop()

@router.post("/{name}/start")
def start_instance(name: str):
    task = AsyncMultipassVM.start_task.delay(name)
    return {"task_id": task.id, "message": "VM starting task submitted"}

@router.post("/{name}/restart")
def restart_instance(name: str):
    return MultipassClientSDK().get_vm(vm_name=name).restart()

@router.post("/")
def launch_instance(data: instance.Instance):
    vm_data = data.dict()
    vm_data["vm_name"] = vm_data.pop("name")  # Renaming 'name' back to 'vm_name'*
    task = async_multipass_client.launch_task.delay(**vm_data)
    return {"task_id": task.id, "message": "VM creation task submitted"}

@router.put("/{name}/mount")
def mount_directory(name: str, mount: mount.Mount):
    return MultipassClientSDK().mount(
        src=mount.source,
        target=f"{name}:{mount.target}",
        uid_maps=mount.uid_map,
        gid_maps=mount.gid_map
    )

@router.delete("/{name}/umount")
def unmount_directory_from_instance(name: str, target: Union[str, None] = None):
    mount=f"{name}:{target}" if target else name
    return MultipassClientSDK().umount(mount)
