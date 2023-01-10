from fastapi import APIRouter, Depends, HTTPException, status
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session
from utils.oauth2 import get_current_user
from database.database import get_db
from utils import schemas
from database import models
from typing import List
from sqlalchemy import and_

router = APIRouter(prefix="/leave", tags=["Leave"])

@router.get('/requests')
def get_leave_requests(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    role = current_user.role
    if role != "hr" or role[:4] != "head":
        leaves = db.query(models.Leave).filter(and_(models.Leave.employee == current_user.id, models.Leave.accepted == None)).all()
        return leaves
    if role != "hr":
        leaves = db.query(models.Leave).filter(and_(models.Leave.department == role[4:], models.Leave.allowed == None)).all()
        return leaves
    leaves = db.query(models.Leave).filter(and_(models.Leave.allowed == True, models.Leave.accepted == None)).all()

    return leaves

@router.get('/given')
def get_given_leaves(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    role = current_user.role
    if role != "hr" or role[:4] != "head":
        leaves = db.query(models.Leave).filter(and_(models.Leave.employee == current_user.id, models.Leave.accepted == True)).all()
        return leaves
    if role != "hr":
        leaves = db.query(models.Leave).filter(and_(models.Leave.department == role[4:], models.Leave.accepted == True)).all()
        return leaves
    leaves = db.query(models.Leave).filter(models.Leave.accepted == True).all()

    return leaves

@router.get('/denied')
def get_given_leaves(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    role = current_user.role
    if role != "hr" or role[:4] != "head":
        leaves = db.query(models.Leave).filter(and_(models.Leave.employee == current_user.id, models.Leave.accepted == False)).all()
        return leaves
    if role != "hr":
        leaves = db.query(models.Leave).filter(and_(models.Leave.department == role[4:], models.Leave.accepted == False)).all()
        return leaves
    leaves = db.query(models.Leave).filter(models.Leave.accepted == False).all()

    return leaves

@router.post('/requests')
def ask_leave(leave: schemas.Leave ,db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    if current_user.role == "hr":
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    department = current_user.role[4:]
    new_leave = models.Leave(**leave.dict(), employee=current_user.id, department=department)
    db.add(new_leave)
    db.commit()
    db.refresh(new_leave)
    announcement = models.Announcement(table="leaves", id_in_table=new_leave.id)
    db.add(announcement)
    db.commit()
    db.refresh(announcement)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Requested"})

@router.post('/given')
def give_leave(leave: schemas.LeaveUpdate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    if current_user.role == "hr":
        query = db.query(models.Leave).filter(models.Leave.id == leave.id)
        query_result = query.first()
        if query_result == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        if query_result.allowed != True:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        leave_dict = leave.dict()
        leave_dict["accepted"] == True
        query.update(leave_dict)
        db.commit()
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "finished"})
    elif current_user.role[:4] == "head":
        query = db.query(models.Leave).filter(models.Leave.id == leave.id)
        query_result = query.first()
        if query_result == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        leave_dict["allowed"] == True
        query.update(leave_dict)
        db.commit()
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "finished"})
    else: raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

@router.post('/denied')
def give_leave(leave: schemas.LeaveUpdate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    if current_user.role == "hr":
        query = db.query(models.Leave).filter(models.Leave.id == leave.id)
        query_result = query.first()
        if query_result == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        leave_dict = leave.dict()
        leave_dict["accepted"] = False
        query.update(leave_dict)
        db.commit()
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "finished"})
    elif current_user.role[:4] == "head":
        query = db.query(models.Leave).filter(models.Leave.id == leave.id)
        query_result = query.first()
        if query_result == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        leave_dict = leave.dict()
        leave_dict["allowed"] == False
        query.update(leave)
        db.commit()
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "finished"})
    else: raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)