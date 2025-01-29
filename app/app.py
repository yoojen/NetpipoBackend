from app.models import User, Employee
from app import db
from flask import request, abort, make_response
from flask_restful import Resource, fields, marshal
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from flask_restful import Resource
from app.helper import jwt_optional_for_tests
from dotenv import load_dotenv
import os


app = Flask(__name__)
jwt = JWTManager(app)
api = Api(app)


load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('FLASK_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('FLASK_SECURITY_KEY')
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
db.init_app(app)


employee_fields = {
    "id": fields.Integer,
    "email": fields.String,
    "name": fields.String,
    "salary": fields.Integer
}


class EmployeeResource(Resource):

    def get(self, employee_id=None):
        if employee_id:
            try:
                employee = Employee.find_employee(employee_id)
                if not employee:
                    return make_response({"message": "No employee found"}, 404)
                return make_response({"message": "Retrieved Successfully", "data": marshal(employee, employee_fields)}, 200)
            except Exception as e:
                print(e)
                abort(400, "Something went wrong")

        employees = db.session.query(Employee).all()
        return make_response({
            "message": "Retrieved Successfully",
            "employees": [marshal(e, employee_fields) for e in employees]
        }, 200)

    @jwt_optional_for_tests
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

        return make_response({"message": f"User created with ID {employee.id}", "employee": marshal(employee, employee_fields)}, 201)

    @jwt_optional_for_tests
    def put(self, employee_id=None):
        if not employee_id:
            return make_response({"message": "Please provide an id"}, 400)
        employee = Employee.find_employee(employee_id)

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
        return make_response({"message": "Employee is updated successfully", "employee": marshal(employee, employee_fields)}, 200)

    @jwt_optional_for_tests
    def delete(self, employee_id=None):
        if not employee_id:
            return {"message": "Provide an employee id"}
        try:
            employee = Employee.find_employee(employee_id)
            if not employee:
                return make_response({"message": "No employee found"}, 404)

            db.session.delete(employee)
            db.session.commit()
            return make_response({}, 204)
        except Exception as e:
            print(e)
            return make_response({"message": "Something went wrong, unable to delete"}, 400)


class UserResource(Resource):

    @jwt_optional_for_tests
    def put(self, user_id=None):
        if not user_id:
            return make_response({"message": "Please provide user id"}, 400)

        user = User.find_user(user_id)

        if not user:
            return make_response({"message": "No user found"}, 404)

        exist_email = User.find_existing_email(request.form.get('email'))
        if exist_email:
            abort(400, "Email is already registered")

        try:
            for k, v in dict(request.form).items():
                if k == 'password':
                    return make_response({"message": "Password change is not implemented"}, 400)
                if hasattr(user, k):
                    if getattr(user, k) == v:
                        continue
                    setattr(user, k, v)

            db.session.commit()
        except Exception as e:
            print(e)
            return make_response({"message": "Something went wrong"}, 400)

        return make_response({"message": "user is updated successfully"}, 200)

    @jwt_optional_for_tests
    def delete(self, user_id):
        if not user_id:
            return {"message": "Provide an user id"}
        user = User.find_user(user_id)
        db.session.delete(user)
        db.session.commit()
        return make_response(204)


class UserRegister(Resource):
    def post(self):
        email = request.form.get('email')
        password = request.form.get('password')

        if (not email) or (not password):
            abort(400, "Email or Password are not available")
        try:
            user = User(email=email, password=password)
            user.create_user_pass_hash()
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            print(e)
            return make_response({"message": "User creation failed"}, 400)

        return make_response({"message": "Account created successfully"}, 201)


class UserLogin(Resource):
    def post(self):
        data = request.form
        email = data.get('email')
        password = data.get('password')

        user = User.find_existing_email(email)
        if not user:
            abort(404, "No user found")
        user_psd = user.check_user_pass_hash(password)

        if (not user) or (not user_psd):
            return make_response({'message': 'Invalid credentials'}), 401

        access_token = create_access_token(identity=str(user.email))
        return make_response({'access_token': access_token, "message": "Access Token generated successfully"}, 200)


api.add_resource(EmployeeResource,
                 '/employees/',
                 '/employees/<int:employee_id>')
api.add_resource(UserResource, '/users/', '/users/<int:user_id>')
api.add_resource(UserRegister, '/auth/register')
api.add_resource(UserLogin, '/auth/login')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
