from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import or_
from starlette.responses import JSONResponse
from utils import schemas, utils, oauth2
from database.database import get_db
from utils.oauth2 import get_current_user
from database import database, models
import boto3
from random import random
import math
from sqlalchemy.sql.expression import text

router = APIRouter(tags=['Authentication'])

client = boto3.client(
    "sns",
    aws_access_key_id="AKIAWCJGOJN2DIEYFHFM",
    aws_secret_access_key="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",
    region_name="us-east-1"
)

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
    list = []
    for i in range(6):
        x = 10 * random()
        y = math.floor(x)
        list.append(str(y))
    otp = ''.join(list)
    new_user = models.User(**user.dict(), verification_code=otp, verification_code_time=text('now()'))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    client.publish(
    PhoneNumber="+250786082841",
    Message= f"Your CUR Verification code is {otp} ",
    MessageAttributes={'AWS.SNS.SMS.SenderID': {'DataType': 'String', 'StringValue': 'CUR' }}
)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Created"})

@router.patch("/verify")
def verify_user(verification: schemas.Verify, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    fetch = db.query(models.User).filter(models.User.id == current_user.id)
    if fetch.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if fetch.first().active == True:
        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED)
    if fetch.first().verification_code == verification.code:
        fetch.update({"Verified": True}, synchronize_session=False)
    else: raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return {"message": 'Verified'}

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