import os
import json
import unittest
from flask_testing import TestCase
from app.app import app, db
from dotenv import load_dotenv

load_dotenv()


class EmployeeTestCase(TestCase):

    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
            'FLASK_DATABASE_URI')
        app.config['TESTING'] = True
        app.config['JWT_SECRET_KEY'] = 'THIS IS SECURITY KEY'
        app.config['SKIP_AUTH'] = True
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_all_employees(self):
        self.client.post('/employees/', data=dict(
            name='Eugene Mutuyimana',
            email='eugene@yahoo.com',
            position="CEO",
            salary=3500
        ))

        response = self.client.get('/employees/')
        res_dict = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(res_dict['employees']), list)

    def test_create_employee(self):
        response = self.client.post('/employees/', data=dict(
            name='Eugene Mutuyimana',
            email='eugene@yahoo.com',
            position="CEO",
            salary=3500
        ))
        res_dict = json.loads(response.data)
        self.assertEqual(res_dict['employee']['email'], 'eugene@yahoo.com')
        self.assertEqual(response.status_code, 201)

    def test_update_employee(self):
        response = self.client.post('/employees/', data=dict(
            name='Eugene Emma',
            email='emma@gmail.com',
            position="HR",
            salary=3500
        ))
        self.assertEqual(response.status_code, 201)

        res_dict = json.loads(response.data)
        employee_id = res_dict['employee']['id']

        update_response = self.client.put(f'/employees/{employee_id}', data=dict(
            email='emma7@gmail.com'
        ))
        update_res_dict = json.loads(update_response.data)
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(
            update_res_dict['employee']['email'], 'emma7@gmail.com')

    def test_delete_employee(self):
        response = self.client.post('/employees/', data=dict(
            name='Eugene M',
            email='eugm@yahoo.com',
            position="CTO",
            salary=3500

        ))
        self.assertEqual(response.status_code, 201)

        response_data = json.loads(response.data)
        employee_id = response_data['employee']['id']

        response = self.client.delete(f'/employees/{employee_id}')
        self.assertEqual(response.status_code, 204)

        # check deletion
        response = self.client.get(f'/employees/{employee_id}')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
