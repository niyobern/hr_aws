from fastapi import FastAPI, status, HTTPException, Depends, APIRouter, Form
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session
from database import models
from utils import schemas, utils, oauth2
from database.database import get_db
from typing import List
from sqlalchemy import and_
import boto3
from database.config import settings
import segno

access_key = settings.aws_access_key
secret_key = settings.aws_secret_key

s3 = boto3.client("s3", 
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key)

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(employee: schemas.Employee, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    image = employee.image
    bucket_name = "ntaweli-hr"
    object_name = f"{current_user.id}_{image.filename}"
    s3.upload_fileobj(image.file, bucket_name, object_name)
    new_user = models.Employee(**employee.dict(), image=object_name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    announcement = models.Announcement(table="employees", id_in_table=new_user.id)
    db.add(announcement)
    db.commit()
    db.refresh(announcement)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Created"})
    
@router.get('/new')
def return_get_all_users(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    if current_user.role == "hr":
        announcements = db.query(models.Announcement).filter(and_(models.Announcement.seen == None, models.Announcement.table == "employees")).all()
        employees = []
        for i in announcements:
            employee = db.query(models.Employee).filter(models.Employee.id == i.id_in_table).first()
            employees.append(employee)
        return employees
    else: 
        employee = db.query(models.Employee).filter(models.Employee.user_id == current_user.id).first()
        if employee != None :
            return JSONResponse(status_code=status.HTTP_200_OK, content=[])
        user = db.query(models.User).filter(models.User.id == current_user.id).first()
        return [{"user_id": user.id, "email": user.email, "phone": user.phone}]
    
@router.get('/')
def return_get_all_users(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    if current_user.role != "hr":
        employee = db.query(models.Employee).filter(models.Employee.user_id == current_user.id).first()
        card = {"name": employee.name, "position": employee.position, "department": employee.department, "type": employee.type, "image": f"https://ntaweli-hr.s3.us-east-2.amazonaws.com/{employee.image}", "qr": f"https://ntaweli-hr.s3.us-east-2.amazonaws.com/qr_{employee.id}.png"}
        return [card]
    employees = db.query(models.Employee).filter(models.Employee.deleted == False).all()
    return employees

@router.get('/card/{id}')
def return_profile(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    employee = db.query(models.Employee).filter(models.Employee.id == id).first()
    card = {"name": employee.name, "position": employee.position, "department": employee.department, "type": employee.type, "image": f"https://ntaweli-hr.s3.us-east-2.amazonaws.com/{employee.image}", "qr": f"https://ntaweli-hr.s3.us-east-2.amazonaws.com/qr_{employee.id}.png"}
    return card

@router.get('/{id}')
def return_profile(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    employee = db.query(models.Employee).filter(models.Employee.id == id).first()
    card = {"name": employee.name, "position": employee.position, "department": employee.department, "type": employee.type, "image": f"https://ntaweli-hr.s3.us-east-2.amazonaws.com/{employee.image}"}
    return employee

@router.patch('/')
def modify_user(employee: schemas.EmployeeUpdate, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    if current_user.role != "hr":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    query = db.query(models.Employee).filter(models.Employee.id == employee.id)
    query_result = query.first()
    if query_result == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if employee.head:
        role = "head" + employee.department
    else: role = "none" + employee.department
    qr_code = segno.make(f"https://imsapi.lavajavahouse.net/users/{employee.id}")
    qr_code.save("qr.png", scale=5)
    s3.upload_file("qr.png", "ntaweli-hr", f"qr_{employee.id}.png")
    query.update(**employee, synchronize_session=False)
    db.commit()
    user_query = db.query(models.User).filter(models.User.id == employee.user_id)
    user_query.update({"role": role}, synchronize_session=False)
    announcement = db.query(models.Announcement).filter(and_(models.Announcement.id_in_table == employee.id, models.Announcement.table == "employees")).first()
    query = db.query(models.Announcement).filter(models.Announcement.id == announcement.id)
    query.update({"seen": True}, synchronize_session=False) 
    return JSONResponse(status_code=200, content={"message": query.first()})

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