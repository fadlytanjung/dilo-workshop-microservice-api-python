# dilo-workshop-microservice-api-python

Minimum JWT, SQLAlchemy API, and Flask-Restful

## Overview

This project is a simple Dog-Owner tracker. The owners are considered Users, and we've set up Users, and roles (among other [things](https://pythonhosted.org/Flask-Security/features.html)) through ```Flask-Security```. The models (found in ```db > models.py```) are declared and managed using ```SQLAlchemy```. The ```Flask-Restful``` API can be seen throughout the project, though the ```dog.py``` and ```owner.py``` files in the ```resources``` directory will be of most use when figuring out how to set up the HTTP methods through class-based methods.

We're using ```Flask-JWT``` for authentication and authorization.

The configuration for ```Flask-migrate``` can be seen in the ```migrate.py``` file in the project root.

## Pip requirements Needed:

- flask
- flask-security
- flask-restful
- flask-cors
- flask-sqlalchemy
- flask-migrate
- flask-script
- flask-jwt
- marshmallow
- marshmallow_jsonapi

install requirements package 

```bash
pip3 install -r requirements.txt
```

## Before Running Server - Set Up Database:

Create your DB in Postgres using the credentials stored in the ```config/base_settings.py``` file (see the ```setup.md``` file for instructions on doing this), and then run the following from the project root:

```bash
python3 migrate.py db init
python3 migrate.py db migrate
python3 migrate.py db upgrade
```

## JSON Request Format When No Authorization Needed
When you request protected route, you should send JWT token for access data:

```
{
  "Authorization":"Bearer {{ jwt_token }}"
}
```

## Protected API Endpoints

As you can see in  the ```user.py``` file, all of the CRUD features for the ```User``` class are protected by the decorator ```jwt_required()```. This means that a valid Authorization token is needed in order to reach those endpoints and perform that logic. In order to get a valid auth token, send a POST request to this url: ```/api/v1/auth``` with the Content-Type Header of ```application/json```, passing in the following:

```
{
    "ownername": "EMAIL",
    "ownerpassword": "PASSWORD"
}
```

**Note**: Rather than the JWT standard of ```"username"``` and ```"password"``` as the authorization keys, we've specified different keys, really just to show that you can. These keys are declared in the respective config files.

Once you send that request, you should get the following back:

```
{
    "access_token": "AUTH_TOKEN"
}
```

Using this token, you can then call the protected endpoints by adding the following headers to your calls:

```
Authorization : JWT AUTH_TOKEN
```

**Note**: Again, you can change the "JWT" value in the Auth header in the config file. We just chose not to in order to not conflict with OAuth2 Bearer tokens (as per the JWT documentation).

