from app.models import Employee
from app import db
from flask import request, abort, make_response
from flask_restful import Resource, fields, marshal, reqparse
from flask import Flask
from flask_restful import Api

from flask_restful import Resource


app = Flask(__name__)
api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:EugeneMysql123.@127.0.0.1:3306/netpipo"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


employee_fields = {
    "email": fields.String,
    "name": fields.String,
    "salary": fields.Integer
}


class EmployeeResource(Resource):
    def get(self, employee_id=None):
        if employee_id:
            try:
                employee = Employee.find_user(employee_id)
                if not employee:
                    return make_response({"message": "No employee found"}, 400)
                return make_response({"message": "Retrieved Successfully", "data": marshal(employee, employee_fields)}, 200)
            except Exception as e:
                print(e)
                abort(400, "Something went wrong")

        employees = db.session.query(Employee).all()
        return make_response({
            "message": "Retrieved Successfully",
            "data": [marshal(e, employee_fields) for e in employees]
        }, 200)

    def post(self):
        name = request.form.get('name')
        email = request.form.get('email')
        position = request.form.get('position')
        salary = request.form.get('salary')

        if (not name) or (not email) or (not position) or (not salary):
            return make_response({"message": "Please provide all required fields"}, 400)

        exist_email = Employee.find_existing_email(email)
        if exist_email:
            return make_response({"message": "The email is already registered"}, 409)

        try:
            employee = Employee(name=name, email=email, salary=salary)
            db.session.add(employee)
            db.session.commit()
        except Exception as e:
            print(e)
            return make_response({"message": "Creating employee failed"}, 400)

        return make_response({"status": f"User created with ID {employee.id}"}, 201)

    def put(self, employee_id=None):
        if not employee_id:
            return make_response({"message": "Please provide an id"}, 400)
        employee = Employee.find_user(employee_id)

        if not employee:
            return make_response({"message": "No employee found"}, 404)

        exist_email = Employee.find_existing_email(request.form.get('email'))
        if exist_email:
            abort(400, "Email is already registered")

        try:
            for k, v in dict(request.form).items():
                if hasattr(employee, k):
                    if getattr(employee, k) == v:
                        continue
                    setattr(employee, k, v)

            db.session.commit()
        except Exception as e:
            print(e)
            return make_response({"message": "Something went wrong"}, 400)
        return make_response({"message": "Employee is updated successfully"}, 200)

    def delete(self, employee_id):
        if not employee_id:
            return {"message": "Provide an employee id"}
        employee = Employee.find_user(employee_id)
        db.session.delete(employee)
        db.session.commit()
        return make_response({"messaage": "Deleted successfully"}, 204)


class AuthResource(Resource):
    pass


api.add_resource(EmployeeResource,
                 '/employees/',
                 '/employees/<int:employee_id>')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
