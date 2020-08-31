#Projects functions

from flask import Response, request
from flask_jwt_extended import jwt_required, get_jwt_identity     #restricting unauthorized user from editing anything in db
from database.models import Project
from flask_restful import Resource
from middlewear.middlewear import check_token

#errors
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
from resources.errors import SchemaValidationError,ForbiddenError, AlreadyExistsError,BadRequestError, NotExistsError, UnauthorizedError

class ProjectsApi(Resource):
    def get(self):              #view all articles - R
        try:
            projects = Project.objects().order_by('-id').to_json()              #descending order
            return Response(projects, status=200)
        except:
            raise BadRequestError

    @jwt_required       #decorator
    def post(self):     #create a project post - C
        try:
            userID = get_jwt_identity()
            token = request.headers['Authorization'].replace('Bearer ', '')
            user = check_token(token, userID)
            if user is None:
                raise ForbiddenError
            else:
                body = request.get_json()
                project = Project(**body).save()           #collection = Class(**body).save()
                id = project.id
                return {'success':'project posted'}, 201
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except UnauthorizedError:
            raise UnauthorizedError
        except Exception as e:
            raise BadRequestError



class ProjectApi(Resource):
    @jwt_required       #decorator
    def delete(self, id):           #delete a project post - D
        try:
            userID = get_jwt_identity()
            token = request.headers['Authorization'].replace('Bearer ', '')
            user = check_token(token, userID)
            if user is None:
                raise ForbiddenError
            else:
                project = Project.objects.get(id=id).delete()
                return {'success':'project deleted'}, 200
        except DoesNotExist:
            raise NotExistsError
        except Exception:
            raise BadRequestError