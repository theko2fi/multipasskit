from fastapi import  APIRouter
from typing import Union, Optional
from multipasskit.api.models import instance, mount
from multipasskit.sdk.multipass import MultipassClientSDK
from multipasskit.api.celerymultipass import AsyncMultipassClient, AsyncMultipassVM
import subprocess
import shlex
from pydantic import BaseModel

class ExecCommand(BaseModel):
    cmd: str
    working_directory: Optional[str] = None

router = APIRouter(prefix='/instances', tags=["instances"])

async_multipass_client = AsyncMultipassClient()

@router.get("/")
def list_instances():
    return MultipassClientSDK().list()

@router.get("/{name}")
def instance_info(name: str):
    return MultipassClientSDK().get_vm(vm_name=name).info()

@router.post("/{name}/exec")
def exec_command(cmd_to_execute: ExecCommand, name: str):
    cmd = ["multipass", "exec"]
    if cmd_to_execute.working_directory:
        cmd += ["--working-directory", cmd_to_execute.working_directory]
    cmd_args = shlex.split(cmd_to_execute.cmd)
    try:
        result = subprocess.run(
            cmd + [name, '--'] + cmd_args,
            check=True,
            capture_output=True
        )
        return {"return_code": result.returncode, "stdout": result.stdout.decode(), "stderr": result.stderr.decode()}
    except subprocess.CalledProcessError as e:
        return {"return_code": e.returncode, "stdout": e.stdout.decode(), "stderr": e.stderr.decode()}

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
    task = AsyncMultipassVM.stop_task.delay(name)
    return {"task_id": task.id, "message": "VM stopping task submitted"}

@router.post("/{name}/start")
def start_instance(name: str):
    task = AsyncMultipassVM.start_task.delay(name)
    return {"task_id": task.id, "message": "VM starting task submitted"}

@router.post("/{name}/restart")
def restart_instance(name: str):
    task = AsyncMultipassVM.restart_task.delay(name)
    return {"task_id": task.id, "message": "VM restarting task submitted"}

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
