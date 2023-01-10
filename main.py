from fastapi import FastAPI, Depends, status
from starlette.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from database import models
from alembic import command
from database.database import engine
from routes import users, auth, payroll
from alembic.command import revision, upgrade
from alembic.config import Config
from routes import auth, administration, leave, payroll, users
app = FastAPI()
alembic_cfg = Config("alembic.ini")

# models.Base.metadata.create_all(bind=engine)
revision(config=alembic_cfg, autogenerate=True)
upgrade(config=alembic_cfg, revision="head")

app.include_router(auth.router)
app.include_router(administration.router)
app.include_router(leave.router)
app.include_router(payroll.router)
app.include_router(users.router)

@app.get('/')
async def index():
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Welcome to our new app"})