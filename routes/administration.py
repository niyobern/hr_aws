from fastapi import APIRouter, Depends, HTTPException, status
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session
from utils.oauth2 import get_current_user
from database.database import get_db
from utils import schemas
from database import models
from typing import List
from sqlalchemy import and_
from utils.utils import make_document
from datetime import datetime

router = APIRouter(prefix="/admin", tags=["Administration"])

@router.get('/new')
def get_announcements(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    if current_user.role == "hr":
        announcements = db.query(models.Announcement).filter(models.Announcement.seen != True).all()
        output = []
        for i in announcements:
            if i.table == "employees":
                action = "New Employee"
                employee = db.query(models.Employee).filter(models.Employee.id == i.id_in_table).first()
                time_created = employee.created_at
                day = str(time_created)[:10]
                time = str(time_created)[11:19]
                output.append({"Action": action, "Date Created": day, "Time Created": time, "Employee": employee})

            if i.table == "leaves":
                action = "Leave Request"
                leave = db.query(models.Leave).filter(models.Leave.id == i.id_in_table).first()
                day = str(time_created)[:10]
                time = str(time_created)[11:19]
                output.append({"Action": action, "Date Created": day, "Time Created": time, "Leave": leave})

            if i.table == "documents":
                action = "Document Request"
                document = db.query(models.Document).filter(models.Document.id == i.id_in_table).first()
                day = str(time_created)[:10]
                time = str(time_created)[11:19]
                output.append({"Action": action, "Date Created": day, "Time Created": time, "Document": document})
        return output


@router.get('/documents')
def get_requests(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    if current_user.role != "hr":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    requests = db.query(models.Document).filter(models.Document.issued == None).all()
    return requests

@router.post('/documents')
def ask_document(document: schemas.Document, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    document_quest = models.Document(document=document.document, employee=current_user.id)
    db.add(document_quest)
    db.commit()
    db.refresh(document_quest)
    announcement = models.Announcement(table="documents", id_in_table=document_quest.id)
    db.add(announcement)
    db.commit()
    db.refresh(document_quest)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "done"})


@router.post('/documents/services/{id}')
def give_document(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    if current_user.role != "hr":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    query = db.query(models.Document).filter(models.Document.id == id)
    document = query.first()
    if document == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    employee_id = document.employee
    document_type = document.document
    date_time = datetime.utcnow()
    s = str(date_time)
    year = s[:4]
    month = s[5:7]
    day = s[8:10]
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    gender = employee.gender
    if employee.qualification == "doctor":
        title = "Dr."
    elif gender == "male":
        title = "Mr"
    else: title == "Mrs"
    make_document(date=day, month=month, year=year, title=title, date_from=employee.start, date_to=employee.end) 
    dict = {"id": id, "employee": employee, "document": document_type, "issued": True}
    query.update(dict)
    db.commit()
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "done"})
