from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session
from database import models
from utils import schemas, utils, oauth2
from database.database import get_db
from typing import List
from sqlalchemy import and_
router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(employee: schemas.Employee, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    new_user = models.Employee(**employee.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    announcement = models.Announcement(table="employees", id_in_db=new_user.id)
    db.add(announcement)
    db.commit()
    db.refresh(announcement)

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Created"})
    
@router.get('/')
def return_get_all_users(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    if current_user.role != "hr":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    employees = db.query(models.Employee).filter(models.Employee.deleted == False).all()
    return employees

@router.get('/new')
def return_get_all_users(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    if current_user.role == "hr":
        announcements = db.query(models.Announcement).filter(and_(models.Announcement.seen != True), models.Announcement.table == "employees").all()
        employees = []
        for i in announcements:
            employee = db.query(models.Employee).filter(models.Employee.id == i.id_in_table).fist()
            employees.append(employee)
        return employees
    else: 
        employee = db.query(models.Employee).filter(models.Employee.user_id == current_user.id).first()
        announcement = db.query(models.Announcement).filter(and_(models.Announcement.table == "employees"), models.Announcement.seen != True).filter(models.Announcement.id_in_table == employee.id).first()
        if announcement != None:
            return [employee]
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": []})

@router.get('/{id}')
def return_profile(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    employee = db.query(models.Employee).filter(models.Employee.id == id).first()
    return employee

@router.patch('/')
def modify_user(employee: schemas.EmployeeUpdate, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    if current_user.role != "hr":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    query = db.query(models.Employee.id == employee.id)
    query_result = query.first()
    if query_result == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if employee.head:
        role = "head" + employee.department
    query.update(employee, synchronize_session=False)
    db.commit()
    user_query = db.query(models.User).filter(models.User.id == employee.user_id)
    user_query.update({"role": role}, synchronize_session=False)
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