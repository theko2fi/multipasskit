## Usage

Here is an example of how to use the SDK:

```python
from multipasskit.sdk.multipass import MultipassClientSDK

client = MultipassClientSDK()

# Launch a new instance
vm_name = client.launch(cpu=2, mem="4G", disk="10G", image="ubuntu-lts")

# Get information about the instance
info = client.get_vm(vm_name).info()
print(info)

# Stop the instance
client.get_vm(vm_name).stop()

# Start the instance
client.get_vm(vm_name).start()

# Delete the instance
client.get_vm(vm_name).delete(purge=True)
```