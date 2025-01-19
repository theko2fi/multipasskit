from fastapi import  APIRouter
import json
from multipasskit.sdk.multipass import MultipassClientSDK
from typing import Union

router = APIRouter(prefix='/configs', tags=["configs"])

@router.get("/")
def get_config_settings(key: Union[str, None] = None):
    return MultipassClientSDK().get(key)

@router.get("/keys")
def list_available_settings_keys():
    output_bytes = MultipassClientSDK().get(keys=True)
    # Decode the bytes to a string and Split the string by line breaks
    output_str = output_bytes.decode('utf-8').splitlines()
    # Convert to JSON object (list of keys)
    return json.dumps(output_str)