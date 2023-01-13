from typing import List
from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional

class Employee(BaseModel):
    gender: str
    id: Optional[int]
    user_id: Optional[int]
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
    department: Optional[str]
    head: Optional[bool]

class EmployeeUpdate(BaseModel):
    user_id : int
    id: int
    start: str
    salary : str
    position : str
    deleted : Optional[str]
    type : str
    department : str
    head: Optional[bool]


class EmployeeIn(BaseModel):
    name : str
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

class User(BaseModel):
    name: str
    email: EmailStr
    phone: str
    id: int
    role: Optional[str]
    active: Optional[bool]

class Verify(BaseModel):
    code: str

class UserIn(BaseModel):
    email: EmailStr
    phone: str
    password: str

class Leave(BaseModel):   
    type: str
    start: str 
    end: str
    reason: str

class LeaveUpdate(BaseModel):
    id: int
    feedback: Optional[str]

class Document(BaseModel):
    document: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]


