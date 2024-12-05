from sqlalchemy import Column, String, Enum, DateTime
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import enum
import uuid
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Role(enum.Enum):
  ADMIN = 'admin'
  EMPLOYEE = 'employee'

class Employee(Base):
  __tablename__ = 'employees'

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
  name = Column(String, nullable=False)
  email = Column(String, nullable=False)
  password = Column(String, nullable=False)
  role = Column(Enum(Role), nullable=False)

  created_at = Column(DateTime, default=func.now(), nullable=False)
  updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
  deleted_at = Column(DateTime, nullable=True)