# dilo-workshop-microservice-api-python

Minimum JWT, SQLAlchemy API, and Flask-Restful

## Overview
This project was created for dilo workshop microservice API.

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

Create your DB in Postgres or MySQL and setting the configuration in ```.env```  file , you can see ```env.example ``` to see the example of file, and then run the following from the project root:

```bash
python3 migrate.py db init
python3 migrate.py db migrate
python3 migrate.py db upgrade
```

## Running App 

Running this app with following command:

```
python3 main.py
```

Using this token, you can then call the protected endpoints by adding the following headers to your calls:

```
Authorization : JWT AUTH_TOKEN
```

**Note**: Again, you can change the "JWT" value in the Auth header in the config file. We just chose not to in order to not conflict with OAuth2 Bearer tokens (as per the JWT documentation).

