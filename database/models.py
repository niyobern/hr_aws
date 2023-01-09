import enum
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, ARRAY, Float, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, nullable=False, primary_key=True)
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
    deleted = Column(Boolean)
    type = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Bonus(Base):
    __tablename__ = "bonuses"
    id = Column(Integer, nullable=False, primary_key=True)
    user = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Float, nullable=False)
    start = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    end = Column(TIMESTAMP(timezone=True), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email: Column(String, nullable=False, unique=True)
    password: Column(String, nullable=False)
    active: Column(Boolean)
    role: Column(String)

class Leave(Base):
    __tablename__ = "leaves"
    id = Column(Integer, primary_key=True, nullable=False)
    user = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    type = Column(String, nullable=False)
    start = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    end = Column(TIMESTAMP(timezone=True), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Payroll(Base):
    __tablename__ = "payrolls"
    id = Column(Integer, primary_key=True, nullable=False)
    period = Column(String, nullable=False)
    user = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    amount_due = Column(Float, nullable=False)
    amount_paid = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Radiant(Base):
    __tablename__ = "radiant"
    id = Column(Integer, primary_key=True, unique=True)
    user = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable = False)
    duration = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Timetable(Base):
    __tablename__ = "timetable"
    id = Column(Integer, primary_key=True, unique=True)
    user = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable = False)
    duration = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))