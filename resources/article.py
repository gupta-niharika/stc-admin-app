# Article's functions

from flask import Response, request
from flask_jwt_extended import jwt_required, get_jwt_identity         #restricting unauthorized user from editing anything in db
from database.models import Article
from flask_restful import Resource
from middlewear.middlewear import check_token

#errors and exceptions
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
from resources.errors import SchemaValidationError,ForbiddenError, AlreadyExistsError, BadRequestError, NotExistsError, UnauthorizedError

class ArticlesApi(Resource):
    @jwt_required      #decorator
    def post(self):             #create an article - C
        try:
            userID = get_jwt_identity()
            token = request.headers['Authorization'].replace('Bearer ', '')
            user = check_token(token, userID)
            if user is None:
                raise ForbiddenError
            else:
                body = request.get_json()
                article = Article(**body).save()          #collection = Class(**body).save()
                id = article.id
                return {'success':'article post created'}, 201
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except UnauthorizedError:
            raise UnauthorizedError
        except Exception as e:
            raise BadRequestError

class ArticleApi(Resource):    #separately banaye coz isme id padegi url me hi during delete
    @jwt_required       #decorator
    def delete(self, id):               #delete an article - D
        try:
            userID = get_jwt_identity()
            token = request.headers['Authorization'].replace('Bearer ', '')
            user = check_token(token, userID)
            if user is None:
                raise ForbiddenError
            else:
                article = Article.objects.get(id=id).delete()
                return {'success':'article deleted'}, 200
        except DoesNotExist:
            raise NotExistsError
        except Exception:
            raise BadRequestError

class ArticleGApi(Resource):
    def get(self, domain):                      #view all articles - R
        try:
            articles = Article.objects(domain=domain).order_by('-id').to_json()              #descending order, limit does pagination
            return Response(articles, status=200)
        except:
            raise BadRequestError
