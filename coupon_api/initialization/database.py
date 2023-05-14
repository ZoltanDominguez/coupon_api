from typing import Optional

from sqlalchemy.engine import Engine
from sqlmodel import Session, SQLModel, create_engine

engine: Optional[Engine] = None


def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    global engine  # pylint: disable=W0603
    sqlite_file_name = "database.db"
    sqlite_url = f"sqlite:///{sqlite_file_name}"
    connect_args = {"check_same_thread": False}
    engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)
    SQLModel.metadata.create_all(engine)
