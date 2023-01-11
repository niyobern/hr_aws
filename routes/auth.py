from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import or_
from starlette.responses import JSONResponse
from utils import schemas, utils, oauth2
from database.database import get_db
from utils.oauth2 import get_current_user
from database import database, models

router = APIRouter(tags=['Authentication'])

@router.get('/current')
def get_user_info(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return JSONResponse(status_code=status.HTTP_200_OK, content={"Id": current_user.id, "Email": current_user.email, "Role": current_user.role})

@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(or_(models.User.email == user_credentials.username, models.User.phone == user_credentials.username)).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Username")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Password")

    # create a token
    # return token

    access_token = oauth2.create_access_token(data={"user_id": user.id})
    if user.email == "berniyo@outlook.com":
        return {"access_token": access_token, "token_type": "Bearer"}

    return f"Bearer {access_token}"


@router.post("/register", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserIn, db: Session = Depends(get_db)):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Created"})

@router.post("/hr", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserIn, db: Session = Depends(get_db)):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    role = "hr"
    user_dict = user.dict()
    user_dict["role"] = role
    user_dict["active"] = True
    new_user = models.User(**user_dict)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Created"})