from fastapi import  APIRouter
from multipasskit.sdk.multipass import MultipassClientSDK

router = APIRouter(prefix='/networks', tags=["networks"])

@router.get("/")
def list_networks():
    return MultipassClientSDK().networks()