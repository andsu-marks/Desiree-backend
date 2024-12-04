from flask import Flask
from flask_cors import CORS
from app.routes.routes import employees

def create_app():
  app = Flask(__name__)
  CORS(app)

  app.register_blueprint(employees)

  return app