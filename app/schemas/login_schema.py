from marshmallow import fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class LoginSchema(SQLAlchemyAutoSchema):
  email = fields.Email(required=True)
  password = fields.String(required=True, validate=validate.Length(min=8, error="Password needs at least 8 characters"))

login_schema = LoginSchema()