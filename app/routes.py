from flask import Blueprint, jsonify, request
from app.services import list_employees, create_employee,update_employee,remove_employee,fetch_employee_by_id
from app.exceptions import EmployeeNotFoundError

employees = Blueprint('employees', __name__)

@employees.route('/employees', methods=['GET'])
def get_employees():
  employees = list_employees()
  return jsonify(employees), 200

@employees.route('/employees', methods=['POST'])
def post_employee():
  data = request.get_json()
  new_employee = create_employee(data)
  return jsonify(new_employee),201

@employees.route('/employees/<id>', methods=['GET'])
def get_employee_by_id(id):
  employee = fetch_employee_by_id(id)
  return jsonify(employee), 200

@employees.route('/employees/<id>', methods=['PUT'])
def put_employee(id):
  data = request.get_json()
  if not data:
    return jsonify({ "error": "Invalid input" }), 400
  
  try:
    updated_employee = update_employee(data, id)
    return jsonify(updated_employee), 200
  except EmployeeNotFoundError as e:
    return jsonify({"error": str(e)}), 404
  
@employees.route('/employees/<id>', methods=['DELETE'])
def delete_employee(id):
  try:
    remove_employee(id)
    return '', 204
  except EmployeeNotFoundError as e:
    return jsonify({"error": str(e)}), 404
