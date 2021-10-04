from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer, UserLoginSerializer, UserActionSerializer
from rest_framework import status
from .helpers import token_auth


@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_user(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@token_auth
def user_management(request, user):
    if request.method == "GET":
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        serializer = UserActionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(user, serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        serializer = UserActionSerializer(user)
        serializer.delete(user)
        return Response({"success":True}, status=status.HTTP_200_OK)

    return Response(serializer.data, status=status.HTTP_200_OK)
