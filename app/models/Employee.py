from sqlalchemy import Column, Integer, Float, String, DateTime, Date

from backend.Base import Base


class Employee(Base):
    '''
    Model class for Employee table.
    '''
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True, nullable=False)
    full_name = Column(String, nullable=False)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    salary = Column(Float, nullable=False)
    next_salary_increase = Column(Date)
    token = Column(String, unique=True)
    last_token_update = Column(DateTime)
