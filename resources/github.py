#Github ke functions idhar hain

from flask import Response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.models import Github
from flask_restful import Resource
from database.db import db
from middlewear.middlewear import check_token

#errors
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
from resources.errors import SchemaValidationError,ForbiddenError, AlreadyExistsError,BadRequestError, NotExistsError, UnauthorizedError

class GithubsApi(Resource):
    def get(self):
        try:
            githubs = Github.objects().order_by('-id').to_json()                #descending order
            return Response(githubs, status=200)
        except:
            raise BadRequestError

    @jwt_required   #decorator
    def post(self):
        try:
            userID = get_jwt_identity()
            token = request.headers['Authorization'].replace('Bearer ', '')
            user = check_token(token, userID)
            if user is None:
                raise ForbiddenError
            else:
                body = request.get_json()
                github = Github(**body).save()          #collection = Class(**body).save()
                id = github.id
                return {'success':'github posted'}, 201
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except UnauthorizedError:
            raise UnauthorizedError
        except Exception as e:
            raise BadRequestError

class GithubApi(Resource):
    @jwt_required           #decorator
    def delete(self, id):           #delete a github post - D
        try:
            userID = get_jwt_identity()
            token = request.headers['Authorization'].replace('Bearer ', '')
            user = check_token(token, userID)
            if user is None:
                raise ForbiddenError
            else:
                github= Github.objects.get(id=id).delete()
                return {'success':'github post deleted'}, 200
        except DoesNotExist:
            raise NotExistsError
        except Exception:
            raise BadRequestError