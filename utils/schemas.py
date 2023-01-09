from typing import List
from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional

class Employee(BaseModel):
    name : str
    email : str
    phone : str
    qualification : str
    birth_district : str
    birth_sector : str
    birth_cell : str
    birth_village : str
    home_district : str
    home_sector : str
    home_cell : str
    home_village : str
    father : str
    mother : str
    salary : Optional[float]
    position : Optional[str]
    deleted : Optional[str]
    type : Optional[str]



class User(BaseModel):
    name: str
    email: EmailStr
    id: int


