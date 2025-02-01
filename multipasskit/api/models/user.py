import uuid
from sqlmodel import Field, SQLModel


# Shared properties
class UserBase(SQLModel):
    username: str = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)

class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str

# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)

# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID