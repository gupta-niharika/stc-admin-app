#Resources's functions are here

from flask import Response, request
from flask_jwt_extended import jwt_required, get_jwt_identity     #restricting unauthorized user from editing anything in db
from database.models import Resources
from flask_restful import Resource
from middlewear.middlewear import check_token

#errors
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
from resources.errors import SchemaValidationError, ForbiddenError, AlreadyExistsError,BadRequestError, NotExistsError, UnauthorizedError

class ResourcesApi(Resource):
    @jwt_required       #decorator
    def post(self):      #create a resource post - C
        try:
            userID = get_jwt_identity()
            token = request.headers['Authorization'].replace('Bearer ', '')
            user = check_token(token, userID)
            if user is None:
                raise ForbiddenError
            else:
                body = request.get_json()
                res = Resources(**body).save()       #collection = Class(**body).save()
                id = res.id
                return {'success':'resource posted'}, 201
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except UnauthorizedError:
            raise UnauthorizedError
        except Exception as e:
            raise BadRequestError


class ResourceDApi(Resource):
    @jwt_required
    def delete(self,id):        #delete a resource post - D
        try:
            userID = get_jwt_identity()
            token = request.headers['Authorization'].replace('Bearer ', '')
            user = check_token(token, userID)
            if user is None:
                raise ForbiddenError
            else:
                res = Resources.objects.get(id=id).delete()
                return {'success':'resource deleted'}, 200
        except DoesNotExist:
            raise NotExistsError
        except Exception:
            raise BadRequestError

class ResourceGApi(Resource):
    def get(self, domain):          #view all posts - R
        try:
            resourceslist = Resources.objects(domain=domain).order_by('-id').to_json()       #descending order
            return Response(resourceslist, status=200)
        except:
            raise BadRequestError