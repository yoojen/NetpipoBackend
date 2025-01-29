from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class EmployeeResource(Resource):
    def get(self, employee_id=None):
        if not employee_id:
            return {"status": "There is no id"}
        # find employee in db
        return {"status": f"There is an Id {employee_id}"}

    def post(self):
        name = request.form['name']
        email = request.form['email']
        position = request.form['position']
        salary = request.form['salary']

        if (not name) or (not email) or (not position) or (not salary):
            return {"status": "It is not okay here"}
        return {"status": "We are creating user..."}

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


api.add_resource(EmployeeResource, '/employees',
                 '/employees/<string:employee_id>', endpoint='all_employees')
# api.add_resource(EmployeeResource,
#                  '/employees<string:employee_id>', endpoint='single_employee')
if __name__ == '__main__':
    app.run(debug=True)
