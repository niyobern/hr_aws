from typing import List
from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional

class User(BaseModel):
    name: str
    email: EmailStr
    qualification: str
    phone: str
    birth_place: str
    home: str
    mother: str
    father: str


