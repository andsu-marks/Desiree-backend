from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.services import list_employees, create_employee, update_employee, remove_employee, fetch_employee_by_id
from app.exceptions.employee_error import EmployeeError

employees = Blueprint('employees', __name__)

@employees.route('/employees', methods=['GET'])
@jwt_required()
def get_employees():
  employees = list_employees()
  return jsonify(employees), 200

@employees.route('/employees', methods=['POST'])
@jwt_required()
def post_employee():
  data = request.get_json()
  new_employee = create_employee(data)
  return jsonify(new_employee),201

@employees.route('/employees/<id>', methods=['GET'])
@jwt_required()
def get_employee_by_id(id):
  employee = fetch_employee_by_id(id)
  return jsonify(employee), 200

@employees.route('/employees/<id>', methods=['PUT'])
@jwt_required()
def put_employee(id):
  data = request.get_json()
  if not data:
    return jsonify({ "error": "Invalid input" }), 400
  
  try:
    updated_employee = update_employee(data, id)
    return jsonify(updated_employee), 200
  except EmployeeError as e:
    return jsonify({"error": str(e)}), 404
  
@employees.route('/employees/<id>', methods=['DELETE'])
@jwt_required()
def delete_employee(id):
  try:
    remove_employee(id)
    return '', 204
  except EmployeeError as e:
    return jsonify({"error": str(e)}), 404
