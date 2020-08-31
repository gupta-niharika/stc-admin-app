#Event ke functions idhar hain

from flask import Response, request
from flask_jwt_extended import jwt_required, get_jwt_identity     #restricting unauthorized user from editing anything in db
from database.models import Event
from flask_restful import Resource
from middlewear.middlewear import check_token

#errors
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
from resources.errors import SchemaValidationError,ForbiddenError, AlreadyExistsError, BadRequestError, NotExistsError, UnauthorizedError

class EventsApi(Resource):
    def get(self):          #view all events - R
        try:
            events = Event.objects().order_by('-id').to_json()          #descending order
            return Response(events, status=200)
        except:
            raise BadRequestError

    @jwt_required           #decorator
    def post(self):         #create an event post - C
        try:
            userID = get_jwt_identity()
            token = request.headers['Authorization'].replace('Bearer ', '')
            user = check_token(token, userID)
            if user is None:
                raise ForbiddenError
            else:
                body = request.get_json()
                event = Event(**body).save()        #collection = Class(**body).save()
                id = event.id
                return {'success':'event posted'}, 201
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except UnauthorizedError:
            raise UnauthorizedError
        except Exception as e:
            raise BadRequestError



class EventApi(Resource):
    @jwt_required              #decorator
    def delete(self, id):       #delete an event - D
        try:
            userID = get_jwt_identity()
            token = request.headers['Authorization'].replace('Bearer ', '')
            user = check_token(token, userID)
            if user is None:
                raise ForbiddenError
            else:
                event = Event.objects.get(id=id).delete()
                return {'success':'event deleted'}, 200
        except DoesNotExist:
            raise NotExistsError
        except Exception:
            raise BadRequestError