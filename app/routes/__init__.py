from flask_cors import CORS
from flask_restful import Api
from flask import Blueprint, abort, jsonify
from app.api.user.controller import UserService
from app.api.auth.controller import AuthRegister, AuthLogin


# Declare the blueprint
v1 = Blueprint('v1', __name__)

# Set up cross-scripting allowed
CORS(v1)

# Set up the API and init the blueprint
api = Api(v1)

# Set the default route
@v1.route('/')
def show():
    return {"status":True,"message":"Welcome to Users API"},200

#############################################
#              Routes Url                   #
#############################################

# Users
api.add_resource(UserService, '/user/<string:username>')
api.add_resource(AuthRegister, '/register')
api.add_resource(AuthLogin, '/login')


