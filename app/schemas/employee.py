from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.model import Employee

class EmployeeSchema(SQLAlchemyAutoSchema):
  class Meta:
    model = Employee
    load_instance = True
    exclude = ('password',)

employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)