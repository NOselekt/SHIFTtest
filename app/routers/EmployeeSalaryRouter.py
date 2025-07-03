from fastapi import HTTPException, Request, Form, APIRouter, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
import os
import binascii
import datetime

from models import Employee
from backend.async_database import get_database


TOKEN_REFRESH_INTERVAL = 300
templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/employee_salary")


async def generate_token(database: Annotated[AsyncSession, Depends(get_database)], login):
    '''
    Generates a token for the employee and inserts it into the database.
    :param database: database to work with.
    :param login: employee's login.
    :return: new employee's token.
    '''
    token = binascii.hexlify(os.urandom(20)).decode()
    try:
        await database.execute(update(Employee).where(Employee.login == login)
                               .values(token=token, last_token_update=datetime.datetime.now()))
        await database.commit()
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))

    return token

async def check_password(employee: Employee = None,
                         password: str = None):
    '''
    Checks employee's login and password.
    :param employee: Employee object.
    :param password: employee's password.
    :return: None.
    '''
    if not employee:
        raise HTTPException(status_code=403,
                            detail="Работника с таким логином нет в базе данных.")
    elif password != employee.password:
        raise HTTPException(status_code=403,
                            detail="Пароль неверный.")


@router.get("/")
async def default_page(request: Request) -> HTMLResponse:

    return templates.TemplateResponse("default_page.html", {"request": request})


@router.post("/login")
async def get_token(database: Annotated[AsyncSession, Depends(get_database)],
                    login: Annotated[str, Form()],
                    password: Annotated[str, Form()]) -> JSONResponse:
    '''
    Returns JSON with new token to the client.
    :param database: database to work with.
    :param login: employee's login.
    :param password: employee's password.
    :return: JSON with token's data.
    '''
    try:
        employee = await database.scalar(select(Employee).where(Employee.login == login))
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))
    await check_password(employee, password)
    token = await generate_token(database, login)

    return JSONResponse({"token": token})


@router.post("/token")
async def get_token(database: Annotated[AsyncSession, Depends(get_database)],
                    token: Annotated[str, Form()]) -> JSONResponse:
    '''
    Returns salary data to the client.
    :param database: database to work with.
    :param token: employee's token.
    :return: employee's salary and the date of the next salary increase.
    '''
    try:
        employee = await database.scalar(select(Employee).where(Employee.token == token))
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))
    if not employee or (datetime.datetime.now() - employee.last_token_update).seconds >= 300:
        raise HTTPException(status_code=403,
                            detail="Неверный токен.")
    next_salary_increase = str(employee.next_salary_increase)

    return JSONResponse({"salary": employee.salary,
                         "next_salary_increase": next_salary_increase})