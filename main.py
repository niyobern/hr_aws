from fastapi import FastAPI, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import models
from alembic import command
from database.database import engine
from utils.schemas import User
from routes import users, auth, payroll
from alembic.command import revision, upgrade
from alembic.config import Config

app = FastAPI()
alembic_cfg = Config("alembic.ini")

models.Base.metadata.create_all(bind=engine)
# revision(alembic_cfg, autogenerate=True)
# upgrade(alembic_cfg,"head")

@app.get('/')
def index():
    return {"message": "Welcome to HR"}