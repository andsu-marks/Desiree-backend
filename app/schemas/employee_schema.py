from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, pre_load, validate, ValidationError
from werkzeug.security import generate_password_hash
from app.models.employee import Employee

class EmployeeSchema(SQLAlchemyAutoSchema):

  id = fields.UUID(dump_only=True) 
  name = fields.String(required=True, validate=validate.Length(min=2, error="Name needs at least 2 characters"))
  email = fields.Email(required=True)
  isAdmin = fields.Boolean(required=True)
  password = fields.String(load_only=True, required=True, validate=validate.Length(min=8, error="Password needs at least 8 characters"))
  created_at = fields.DateTime(dump_only=True)  
  updated_at = fields.DateTime(dump_only=True)  
  deleted_at = fields.DateTime(dump_only=True)

  @pre_load
  def hash_password(self, data, **kwargs):
    if 'password' in data:
      if len(data['password']) < 8:
        raise ValidationError('Password needs at least 8 characters')
      data['password'] = generate_password_hash(data['password'])
    return data
    
  class Meta:
    model = Employee
    fields = ('id', 'name', 'email', 'isAdmin', 'password', 'created_at', 'updated_at', 'deleted_at')

employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)