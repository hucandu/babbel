from rest_framework.response import Response
from .models import UserData

def token_auth(func):
    def decorate(request, **kwargs):
        token = request.META.get("HTTP_AUTHORIZATION")
        if not token:
            return Response("UnAuthorized", status=401)
        else:
            token = request.META.get("HTTP_AUTHORIZATION").split(" ")[-1]
            select_query_build = '''
            SELECT u.id,
            u.first_name,
            u.last_name,
            u.username,
            u.password,
            u.profile_picture,
            u.deleted,
            u.created_at
            FROM users_token t, users_userdata u
            WHERE t.user_id = u.id
            AND t.key = %s
            AND u.deleted=false
            '''
            user = [i for i in UserData.objects.raw(select_query_build, [token])]
            if len(user)<1:
                return Response("UnAuthorized", status=401)
            else:
                user = user[0]
        response = func(request, kwargs["id"], user)
        return response
    return decorate
