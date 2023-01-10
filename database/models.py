import enum
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, ARRAY, Float, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=False, unique=True)
    qualification = Column(String, nullable=False)
    birth_district = Column(String, nullable=False)
    birth_sector = Column(String, nullable=False)
    birth_cell = Column(String, nullable=False)
    birth_village = Column(String, nullable=False)
    home_district = Column(String, nullable=False)
    home_sector = Column(String, nullable=False)
    home_cell = Column(String, nullable=False)
    home_village = Column(String, nullable=False)
    father = Column(String, nullable=False)
    mother = Column(String, nullable=False)
    salary = Column(Float)
    position = Column(String)
    department = Column(String)
    head = Column(Boolean)
    deleted = Column(Boolean)
    type = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Bonus(Base):
    __tablename__ = "bonuses"
    id = Column(Integer, nullable=False, primary_key=True)
    employee = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Float, nullable=False)
    start = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    end = Column(TIMESTAMP(timezone=True), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email: Column(String, nullable=False, unique=True)
    phone: Column(String, nullable=False, unique=True)
    password: Column(String, nullable=False)
    active: Column(Boolean)
    role: Column(String)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Leave(Base):
    __tablename__ = "leaves"
    id = Column(Integer, primary_key=True, nullable=False)
    employee = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    department = Column(String, ForeignKey("employees.department"), nullable=False)
    type = Column(String, nullable=False)
    start = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    end = Column(TIMESTAMP(timezone=True), nullable=False)
    accepted = Column(Boolean)
    allowed = Column(Boolean)
    feedback = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    

class Payroll(Base):
    __tablename__ = "payrolls"
    id = Column(Integer, primary_key=True, nullable=False)
    period = Column(String, nullable=False)
    employee = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    amount_due = Column(Float, nullable=False)
    amount_paid = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Radiant(Base):
    __tablename__ = "radiant"
    id = Column(Integer, primary_key=True, unique=True)
    employee = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable = False)
    duration = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Announcement(Base):
    __tablename__ = "announcements"
    id = Column(Integer, primary_key=True, unique=True)
    table = Column(String, nullable=False)
    id_in_table = Column(Integer, nullable=False)
    seen = Column(Boolean)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, unique=True)
    employee = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    document = Column(String, nullable=False)
    issued = Column(Boolean)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))