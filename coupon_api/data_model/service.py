from typing import Optional

from sqlmodel import Field, SQLModel


class ServiceGroup(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str


class Service(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    service_group_id: int = Field(default=None, foreign_key="servicegroup.id")
    name: str
    description: str
    price: int
