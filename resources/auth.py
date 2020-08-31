#API endpoint for signup
#from flask import request
from flask import Response, request
from flask_jwt_extended import create_access_token          #token created every time logged in
from database.models import User
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime
from middlewear.middlewear import check_token

#errors
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
from resources.errors import SchemaValidationError,ForbiddenError, AlreadyExistsError,BadRequestError, NotExistsError, EmailAlreadyExistsError, UnauthorizedError

class SignupApi(Resource):
    def post(self):
        try:
            body = request.get_json()       #getting json objects (postman 'ch)
            user = User(**body)             #collection = Class(**body).save()
            user.hash_password()            #user ke password ko hash kar dega yeh - fn in models is called
            user.save()
            id=user.id
            return {'success':'signed up successfully'}, 200
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except NotUniqueError:
            raise EmailAlreadyExistsError
        except Exception as e:
            raise BadRequestError

class DeleteApi(Resource):
    def delete(self):
        try:
            body = request.get_json()
            tempUser = User.objects.get(email=body['email'])
            tempUser.delete()
            return {"deleted": "true"}, 200
        except:
            raise BadRequestError


class LoginApi(Resource):
    def post(self):
        try:
            body = request.get_json()
            user = User.objects.get(email=body.get('email'))
            authorized = user.check_password(body.get('password'))       #fn in models is called
            if not authorized:
                raise UnauthorizedError
            access_token = create_access_token(identity=str(user.id))
            user.token.append(access_token)
            user.save()
            return {'token': access_token}, 200
        except (UnauthorizedError, DoesNotExist):
            raise UnauthorizedError
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except Exception as e:
            raise BadRequestError

class LogoutApi(Resource):
    @jwt_required
    def post(self):
        try:
            userID = get_jwt_identity()
            token = request.headers['Authorization'].replace('Bearer ', '')
            user = check_token(token, userID)
            if user is None:
                raise ForbiddenError
            else:
                user.token.remove(token)
                user.save()
                return {'success':'Logged out successfully'}, 200
        except Exception as e:
            raise BadRequestError