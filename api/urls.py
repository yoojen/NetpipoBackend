from flaskr.app import app, HelloWorld
from flask_restful import Api

api = Api(app)

api.add_resource(HelloWorld, "/test")
