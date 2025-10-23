from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
from pydantic import BaseModel


# SQLAlchemy User model
class UserDB(Base):
    __tablename__ = "users"

    org_user_id = Column(String, primary_key=True, index=True)
    org_id = Column(String, index=True)
    name = Column(String, nullable=False)
    contact_no = Column(String)
    employee_code = Column(String)
    created_date = Column(DateTime, default=datetime.utcnow)
    valid_till = Column(DateTime)


# Pydantic model for request/response
class User(BaseModel):
    org_user_id: str
    org_id: str
    name: str
    contact_no: str
    employee_code: str
    created_date: datetime
    valid_till: datetime

    class Config:
        orm_mode = True  # Enable ORM parsing
