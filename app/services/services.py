from flask import current_app
from sqlalchemy.exc import IntegrityError
from app.exceptions import EmployeeError
from app.models.model import Employee
from app.schemas.employee import employees_schema, employee_schema


def list_employees():
  session = current_app.session
  employees = session.query(Employee).all()
  
  return employees_schema.dump(employees)


def create_employee(data):
  required_fields = ['name', 'email', 'role', 'password']

  if not all(field in data for field in required_fields):
    raise EmployeeError("Missing required fields")
  
  new_employee = Employee(
    name=data['name'],
    email=data['email'],
    role=data['role'],
    password=data['password']
  )

  session = current_app.session  
  session.add(new_employee)
  
  try:
    session.commit()
  except IntegrityError:
    session.rollback()
    raise Exception("Error while creating the employee. Possibly a duplicate entry.")
  
  return employee_schema.dump(new_employee)


def fetch_employee_by_id(id, serialize=True):
  session = current_app.session  
  employee = session.query(Employee).filter_by(id=id).first()

  if not employee:
    raise EmployeeError('Employee not found', 400)
  
  return employee_schema.dump(employee) if serialize else employee


def update_employee(data, id):
  employee = fetch_employee_by_id(id, serialize=False)
  if not employee:
    raise EmployeeError("Employee not found", 400)
  
  allowed_fields = ["name", "email", "role", "password"]

  for field in allowed_fields:
    if field in data:
      setattr(employee, field, data[field])

    
  session = current_app.session
  session.add(employee)
  session.commit()

  return employee_schema.dump(employee)


def remove_employee(id):
  employee = fetch_employee_by_id(id, serialize=False)

  if not employee:
    raise EmployeeError("Employee not found", 400)
  
  session = current_app.session
  session.delete(employee)
  session.commit()
