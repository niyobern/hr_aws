from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from starlette.responses import JSONResponse
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
def create_user(employee: schemas.Employee, db: Session = Depends(get_db)):

    hashed_password = utils.hash(employee.password)
    employee.password = hashed_password
    role = "no_role"
    user_dict = employee.dict()
    user_dict["role"] = role
    new_user = models.User(**user_dict)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
    
@router.get('/', response_model=schemas.EmailStr)
def return_get_all_users(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    if current_user.role != "hr":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    employees = db.query(models.Employee).filter(models.Employee.deleted == False).all()
    return employees

@router.patch('/')
def modify_user(employee: schemas.Employee, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    if current_user.role != "hr":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    query = db.query(models.Employee.id == employee.id)
    query_result = query.first()
    if query_result == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    query.update(employee, synchronize_session=False)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Finished"})

@router.delete('/{id}')
def delete_user(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    if current_user.role != "hr":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    query = db.query(models.Employee).filter(models.Employee == id)
    query_result = query.first()
    if query_result == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    query.delete(synchronize_session=False)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Finished"})