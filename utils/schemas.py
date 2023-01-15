from typing import List
from pydantic import BaseModel, EmailStr
from fastapi import UploadFile, Form, File
from enum import Enum
from typing import Optional

class Employee(BaseModel):
    image: UploadFile = File()
    gender: str = Form()
    id: Optional[int] = Form()
    user_id: Optional[int] = Form()
    name : str = Form()
    email : str = Form()
    phone : str = Form()
    qualification : str = Form()
    birth_district : str = Form()
    birth_sector : str = Form()
    birth_cell : str = Form()
    birth_village : str = Form()
    home_district : str = Form()
    home_sector : str = Form()
    home_cell : str = Form()
    home_village : str = Form()
    father : str = Form()
    mother : str = Form()
    salary : Optional[float] = Form()
    position : Optional[str] = Form()
    deleted : Optional[str] = Form()
    type : Optional[str] = Form()
    department: Optional[str] = Form()
    head: Optional[bool] = Form()

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
    user_id = int
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


