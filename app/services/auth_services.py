from flask import current_app
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from marshmallow import ValidationError
from app.schemas.login_schema import login_schema
from app.models.employee import Employee
from app.exceptions.employee_error import EmployeeError

def authenticate_user(data):
  session = current_app.session

  try:
    validated_data =  login_schema.load(data, session=session)
    email = validated_data['email']
    password = validated_data['password']

    user = session.query(Employee).filter_by(email=email).first()
    if not user or check_password_hash(user.password, password):
      raise ValidationError('Email or password are invalids', 401)
    
    access_token = create_access_token(identity=user.id)
    return access_token
  
  except ValidationError as err:
    raise EmployeeError(f"Validation error: {err.messages}", 400)
  
  except Exception as e:
    raise EmployeeError(f'Unmapped Error: {str(e)}', 500)