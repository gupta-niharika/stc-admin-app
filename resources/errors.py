# Exceptions
class BadRequestError(Exception):
    pass

class SchemaValidationError(Exception):
    pass

class AlreadyExistsError(Exception):
    pass

class NotExistsError(Exception):
    pass

class EmailAlreadyExistsError(Exception):
    pass

class UnauthorizedError(Exception):
    pass

class ExpiredSignatureError(Exception):
    pass

class ForbiddenError(Exception):
    pass

#errors
errors = {
    "BadRequestError": {
        "message": "Bad Request",
        "status": 400
    },
    "SchemaValidationError": {
        "message": "Request is missing required fields",
        "status": 406
    },
    "AlreadyExistsError": {
        "message": "Data with given name already exists",
        "status": 400
    },
    "NotExistsError": {
        "message": "Data with given id does not exist",
        "status": 400
    },
    "EmailAlreadyExistsError": {
        "message": "User with given email address already exists",
        "status": 400
    },
    "UnauthorizedError": {
        "message": "Invalid username or password",
        "status": 401
    },
    "ForbiddenError": {
        "message": "Forbidden user",
        "status": 403
    }
}