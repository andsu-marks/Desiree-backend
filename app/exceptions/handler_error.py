from flask import jsonify
from app.exceptions.employee_error import EmployeeError

def register_error_handlers(app):
    @app.errorhandler(EmployeeError)
    def handle_employee_error(error):
        response = jsonify({"error": str(error)})
        response.status_code = getattr(error, "status_code", 400)
        return response
