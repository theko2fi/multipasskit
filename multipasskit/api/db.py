from sqlmodel import Session, SQLModel, create_engine, select
from fastapi import Depends
from typing_extensions import Annotated
from multipasskit.api.config import settings
from multipasskit.api.models.user import User, UserCreate
from multipasskit.api.auth import create_user

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

def init_db() -> None:
    # Normally, tables should be created with Alembic migrations

    # This works because the models are already imported and registered from api.models
    create_db_and_tables()
    # Create the first superuser
    with Session(engine) as session:
        user = session.exec(
            select(User).where(User.username == settings.FIRST_SUPERUSER)
        ).first()
        if not user:
            user_in = UserCreate(
                username=settings.FIRST_SUPERUSER,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                is_superuser=True,
            )
            user = create_user(session=session, user_create=user_in)