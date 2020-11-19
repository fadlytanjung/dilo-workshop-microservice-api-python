from flask import request, abort
from flask import current_app
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_claims, get_jwt_identity

from app.helper import validation_error, message, err_resp, internal_err_resp

from app import db, jwt
from app.model.user import User, UserSchema

from datetime import datetime


user_schema = UserSchema()

class UserService(Resource):
    
    @jwt_required
    def get(self, username):
        
        """ Get user data by username """
        if not (user := User.query.filter_by(username=username).first()):
            return err_resp("User not found!", "user_404", 404)
        
        try:
            user_data = user_schema.dump(user)
            
            ret = {
                'current_identity': get_jwt_identity(),
                'current_roles': get_jwt_claims()['role']
            }
            print(ret)
            resp = message(True, "User data sent")
            resp["user"] = user_data
            return resp, 200

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

