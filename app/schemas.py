from datetime import datetime
from typing import List
from pydantic import BaseModel


class ContactBaseSchema(BaseModel):
    id: str | None = None
    name: str
    phonenumber: str
    phonenumber_ext: str
    phonenumber_home: str
    category: str | None = None
    createdAt: datetime | None = None
    updatedAt: datetime | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class ListContactResponse(BaseModel):
    status: str
    results: int
    contacts: List[ContactBaseSchema]

# Calls
class CallBaseSchema(BaseModel):
    id: int | None = None
    name: str
    number: str
    category: str | None = None
    receivedOn: datetime | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class ListCallesponse(BaseModel):
    status: str
    results: int
    calls: List[CallBaseSchema]
