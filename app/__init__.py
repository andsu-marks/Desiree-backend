from flask import Flask
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
import os
from app.routes.employee_routes import employees
from app.routes.auth_routes import auth
from app.exceptions.handler_error import register_error_handlers

load_dotenv()

def create_app():
  app = Flask(__name__)

  app.config['SQLALCHEMY_DATABASE_URI'] = f'{os.getenv('DATABASE_URL')}'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

  app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
  app.config["JWT_ACCESS_TOKEN_EXPIRES"] = os.getenv('JWT_SECRET_EXPIRES')
  jwt = JWTManager(app)

  engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
  Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
  app.session = Session()

  register_error_handlers(app)
  app.register_blueprint(auth)
  app.register_blueprint(employees)
  
  CORS(app)

  return app