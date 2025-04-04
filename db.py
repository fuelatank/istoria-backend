from typing import Annotated
from fastapi import Depends
from sqlmodel import create_engine, SQLModel, Session

DATABASE_URL = "postgresql+psycopg://moonshot48:moonshot48@localhost:5432/moonshot48"
engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_db():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_db)]
