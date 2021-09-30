from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer, UserLoginSerializer
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
# @token_auth()
def user_management(request, id):
    return Response({"message": "Hello, world!"})
