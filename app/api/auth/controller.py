from flask import request, abort
from flask_restful import Resource
from flask import current_app
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims

from app.helper import validation_error, message, err_resp, internal_err_resp

from app.model.user import User, UserSchema
from app import db, jwt

from datetime import datetime
from .validate import LoginSchema, RegisterSchema

login_schema = LoginSchema()
register_schema = RegisterSchema()
user_schema = UserSchema()

class UserObject:
    def __init__(self, username, role):
        self.username = username
        self.role = role

class AuthLogin(Resource):
    """ User login endpoint
    User registers then receives the user's information and access_token
    """
    @jwt.user_claims_loader
    def add_claims_to_access_token(user):
        return {'role': user.role}

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user.username

    def post(self):
        """ Login using email and password """
        # Grab the json data
        data = request.get_json()

        # Validate data
        if (errors := login_schema.validate(data)) :
            return validation_error(False, errors), 400

        # Assign vars
        username = data["username"]
        password = data["password"]

        try:
            # Fetch user data
            if not (user := User.query.filter_by(username=username).first()):
                return err_resp(
                    "The email you have entered does not match any account.",
                    "email_404",
                    404,
                )

            elif user and user.verify_password(password):
                user_info = user_schema.dump(user)
                
                if user_info['status'] == 'inactive':
                    return message(False,"your account hasn't been activated"), 401

                user_object = UserObject(username=user.username,role=user.role)
                access_token = create_access_token(identity=user_object)

                resp = message(True, "Successfully logged in.")
                resp["access_token"] = access_token
                resp["user"] = user_info

                return resp, 200

            return err_resp(
                "Failed to log in, password may be incorrect.", "password_invalid", 401
            )

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

class AuthRegister(Resource):
    """ User register endpoint
    User registers then receives the user's information and access_token
    """

    def post(self):
        """ User registration """
        # Grab the json data
        data = request.get_json()

        # Validate data
        if (errors := register_schema.validate(data)) :
            return validation_error(False, errors), 400

        ## Required values
        email = data["email"]
        username = data["username"]
        password = data["password"]

        ## Optional
        data_name = data.get("name")

        # Check if the email is taken
        if User.query.filter_by(email=email).first() is not None:
            return err_resp("Email is already being used.", "email_taken", 403)

        # Check if the username is taken
        if User.query.filter_by(username=username).first() is not None:
            return err_resp("Username is already taken.", "username_taken", 403)

        try:
            new_user = User(
                email=email,
                username=username,
                name=data_name,
                password=password,
                created_at=datetime.utcnow(),
            )

            db.session.add(new_user)
            db.session.flush()

            # Load the new user's info
            user_info = user_schema.dump(new_user)

            # Commit changes to DB
            db.session.commit()

            # Create an access token
            access_token = create_access_token(identity=new_user.id)

            resp = message(True, "User has been registered.")
            resp["access_token"] = access_token
            resp["user"] = user_info

            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()
