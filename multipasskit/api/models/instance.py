from typing import Union
from pydantic import BaseModel

class Instance(BaseModel):
    name: str
    cpu: int = 1
    mem: str = '2G'
    disk: str = '5G'
    cloud_init: Union[str, None] = None
    image: Union[str, None] = 'ubuntu-lts'