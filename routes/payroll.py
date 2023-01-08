from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils.oauth2 import get_current_user
from database.database import get_db
from utils import schemas
from database import models

router = APIRouter(prefix="/payroll", tags=["Payroll"])

@router.get('/{id}')
async def get_payroll(id : int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    base_salary = db.query(models.Employee).filter(models.Employee.id == id).first().salary
    #getting the gross salary and accomodation => hint: accomodation = transport allowances
    accomodation = base_salary / 7
    gross_salary = base_salary + (accomodation * 2)
    bonuses = db.query(models.Bonus). filter(models.Bonus.user == id).all()
    for i in bonuses:
        gross_salary += i
    #getting TPR
    full_time = db.query(models.Employee).filter(models.Employee.id == id).first().type
    if full_time == "part_time":
        tpr = gross_salary * 30 /100
    elif gross_salary <= 60000:
        tpr = 0
    elif 60000 < gross_salary <= 100000:
        tpr = (gross_salary - 60000) * 20 /100
    elif gross_salary > 100000:
        tpr = (gross_salary - 100000) * (30 /100) + 8000
    #RSSB 
    rssb_base = gross_salary - accomodation
    rssb3 = rssb_base * 3 / 100 
    rssb5 = rssb_base * 5 /100
    total_rssb = rssb3 + rssb5
    maternity = (0.3 * gross_salary)
    total_maternity = maternity * 2
    radiant = db.query(models.Radiant).filter(models.Radiant.user == id).first().amount
    net_salary = gross_salary - tpr - rssb3 - maternity - radiant
    cbhi = 4000
    net_to_pay = net_salary - cbhi
    payroll = {"Base Salary": base_salary, 
      "Accomodation": accomodation, 
      "Transport": accomodation, 
      "Bonuses": bonuses, 
      "TPR": tpr, 
      "RSSB Base": rssb_base, 
      "RSSB 3%": rssb3, 
      "RSSB 5%": rssb5, 
      "Total RSSB": total_rssb, 
      "Maternity 0.03%": maternity,
      "Maternity 0.03%": maternity,
      "Total Maternity": total_maternity,
      "Radiant": radiant,
      "Net Salary": net_salary,
      "CBHI": cbhi,
      "Net Salary": net_salary,
      "Net Salary to be Paid": net_to_pay}

    return payroll

