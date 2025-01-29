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
                employee = db.session.query(
                    Employee).filter_by(id=employee_id).first()
                if not employee:
                    print(employee)
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

        exist = db.session.query(Employee).filter_by(email=email).first()
        if exist:
            return make_response({"message": "The email is already registered"}, 409)

        try:
            employee = Employee(name=name, email=email, salary=salary)
            db.session.add(employee)
            db.session.commit()
        except Exception as e:
            print(e)
            return make_response({"message": "Creating employee failed"}, 400)

        return make_response({"status": f"User created with ID {employee.id}"}, 201)

    def update(self, employee_id):
        if not employee_id:
            return {"status": "Please provide an id"}
        # employee = db.findEmployee()
        if 2 < 3:  # if there is no employee
            return {"status": "No employee found"}

        print(f"printing form before actual update {request.form}")
        return {"status": "We are going to update"}

    def delete(self, employee_id):
        if not employee_id:
            return {"status": "Provide an employee id"}
        # employee = db.findEmployee()
        if 2 < 3:  # if there is no employee
            return {"status": "No employee found"}
        return {"status": "We are deleting an employee"}


class AuthResource(Resource):
    pass


api.add_resource(EmployeeResource,
                 '/employees/',
                 '/employees/<int:employee_id>',
                 endpoint='single_employee')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
