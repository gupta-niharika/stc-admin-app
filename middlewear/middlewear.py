from database.models import User


def check_token(userToken, id):
    tempUser = User.objects.get(id=id)
    if userToken in tempUser.token:
        return tempUser
    else:
        return None