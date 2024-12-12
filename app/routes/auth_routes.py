from flask import Blueprint, request, jsonify
from app.services import authenticate_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
  data = request.get_json()
  result = authenticate_user(data)  
  return jsonify({'Token': result}), 200

