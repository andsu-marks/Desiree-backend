from flask import current_app
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from app.exceptions.employee_error import EmployeeError
from app.models.model import Employee
from app.schemas.employee import employees_schema, employee_schema
from flask import jsonify


def list_employees():
  session = current_app.session
  employees = session.query(Employee).all()
  
  return employees_schema.dump(employees)


def create_employee(data):
  session = current_app.session  

  try:
    validated_data = employee_schema.load(data, session=session)
    new_employee = Employee(**validated_data)
  except ValidationError as err:
    raise EmployeeError(f'Validation error: {err.messages}')
  except Exception as e:
    raise EmployeeError(f'Error: {str(e)}')
  
  email_exists = session.query(Employee).filter_by(email=new_employee.email).first()
  if email_exists:
    raise EmployeeError('This e-mail is already in use', 409)

  session.add(new_employee)
  
  try:
    session.commit()
  except IntegrityError:
    session.rollback()
    raise EmployeeError("Error while creating the employee. Possibly a duplicate entry.")
  
  return employee_schema.dump(new_employee)


def fetch_employee_by_id(id, serialize=True):
  session = current_app.session  
  employee = session.query(Employee).filter_by(id=id).first()

  if not employee:
    raise EmployeeError('Employee not found', 400)
  
  return employee_schema.dump(employee) if serialize else employee


def update_employee(data, id):
  employee = fetch_employee_by_id(id, serialize=False)
  session = current_app.session

  try:
    if 'email' in data and data['email'] != employee.email:
      email_exists = session.query(Employee).filter_by(email=data['email']).first()

      if email_exists:
        raise EmployeeError('This e-mail is already in use', 409)
      
    validated_data = employee_schema.load(data, session=session)
    for field in validated_data:
      setattr(employee, field, data[field])

    session.add(employee)
    session.commit()
  except ValidationError as err:
    session.rollback()
    raise EmployeeError(f'Validation error: {err.messages}')
  except Exception as e:
    session.rollback()
    raise EmployeeError(f'Error: {str(e)}')

  return employee_schema.dump(employee)


def remove_employee(id):
  employee = fetch_employee_by_id(id, serialize=False)
  session = current_app.session
  session.delete(employee)
  session.commit()
