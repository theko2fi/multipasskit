from typing import List, Optional
from pydantic import BaseModel, model_validator

class Mount(BaseModel):
    source: str
    target: Optional[str] = None
    uid_map: Optional[List[str]] = []
    gid_map: Optional[List[str]] = []

    @model_validator(mode="before")
    def set_target_to_source(cls, values):
        # Set 'target' to 'source' if 'target' is not provided
        if not values.get('target'):
            values['target'] = values.get('source')
        return values