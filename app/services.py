import uuid
from datetime import datetime
from app.models import fake_db
from app.exceptions import EmployeeNotFoundError


def list_employees():
  return fake_db

def create_employee(data):
  required_fields = ['name', 'email', 'role', 'password']

  if not all(field in data for field in required_fields):
    raise ValueError("Missing required fields")

  new_employee = {
      "id": str(uuid.uuid4()),
      "name": data["name"],
      "email": data["email"],
      "role": data["role"],
      "password": data["password"],
      "created_at": str(datetime.now().date()),
      "updated_at": str(datetime.now().date()),
      "deleted_at": False,
    }
  
  fake_db.append(new_employee)
  return new_employee

def fetch_employee_by_id(id):
  return next((p for p in fake_db if p["id"] == id), None)

def update_employee(data, id):
  employee = fetch_employee_by_id(id)
  if not employee:
    raise EmployeeNotFoundError("Employee not found")
  
  allowed_fields = ["name", "email", "role", "password"]
  for field in allowed_fields:
    if field in data:
      employee[field] = data[field]
  employee["updated_at"] = str(datetime.now().date())
  
  return employee

def remove_employee(id):
  employee = fetch_employee_by_id(id)
  if not employee:
    raise EmployeeNotFoundError("Employee not found")
  
  fake_db.remove(employee)