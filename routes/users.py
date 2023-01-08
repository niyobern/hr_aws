from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from database import models
from utils import schemas, utils, oauth2
from database.database import get_db
from typing import List

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


# /users/
# /users


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.User, db: Session = Depends(get_db)):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    role = "no_role"
    user_dict = user.dict()
    user_dict["role"] = role
    new_user = models.User(**user_dict)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
    
@router.get('/')
def return_get_all_users(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    if current_user.role.value not in ("boss", "deputy_boss"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    users = db.query(models.User).all()
    users_info = []
    for user in users:
        info = {"Name": user.name, "email": user.email, "phone": user.phone, "role": user.role.value, "id": user.id}
        users_info.append(info)
    return users_info