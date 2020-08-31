#Feed function are here

from flask import Response, request, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.models import Feed
from flask_restful import Resource
from middlewear.middlewear import check_token

#errors and exceptions
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
from resources.errors import SchemaValidationError,ForbiddenError, AlreadyExistsError, BadRequestError, NotExistsError, UnauthorizedError

class FeedsApi(Resource):
    def get(self, skip):          #view all feed posts - R
        try:
            print(skip)
            start = int(skip)
            end = start+5                                                          #pagination
            feeds = Feed.objects().order_by('-id')[start:end].to_json()            #descending order
            return Response(feeds, status=200)
        except:
            raise BadRequestError

    @jwt_required               #decorator
    def post(self, skip):             #create a feed post - C
        try:
            userID = get_jwt_identity()
            token = request.headers['Authorization'].replace('Bearer ', '')
            user = check_token(token, userID)
            if user is None:
                raise ForbiddenError
            else:
                body = request.get_json()
                feed = Feed(**body).save()       #collection = Class(**body).save()
                id = feed.id
                return make_response({'success':'feed posted'}, 201)
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except Exception:
            raise UnauthorizedError


class FeedApi(Resource):
    @jwt_required
    def delete(self, id):         #delete a feed post - D
        try:
            userID = get_jwt_identity()
            token = request.headers['Authorization'].replace('Bearer ', '')
            user = check_token(token, userID)
            if user is None:
                raise ForbiddenError
            else:
                feed = Feed.objects.get(id=id).delete()
                return make_response({'success':'feed deleted'}, 200)
        except DoesNotExist:
            raise NotExistsError
        except Exception:
            raise BadRequestError