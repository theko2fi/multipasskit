from fastapi import  APIRouter
from multipasskit.sdk.multipass import MultipassClientSDK

router = APIRouter(prefix='/images', tags=["images"])

@router.get("/")
def list_images():
    return MultipassClientSDK().find()