from rest_framework.response import Response
from .models import UserData

def token_auth(func):
    def decorate(request, **kwargs):
        token = request.META.get("HTTP_AUTHORIZATION")
        if not token:
            return Response("UnAuthorized", status=401)
        else:
            token = request.META.get("HTTP_AUTHORIZATION").split(" ")[-1]
            user = UserData.objects.raw("SELECT * FROM users_userdata WHERE id in (SELECT user_id FROM users_token WHERE key=%s)", [token])
            if len(user)<1:
                return Response("UnAuthorized", status=401)
            else:
                user = user[0]
        response = func(request, user)
        return response
    return decorate
