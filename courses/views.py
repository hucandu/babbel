from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CourseListSerializer, CourseActionSerializer
from rest_framework import status
from users.helpers import token_auth

@api_view(['GET', 'POST', 'DELETE'])
@token_auth
def course_list(request, user):
    if request.method == "GET":
        serializer = CourseListSerializer()
        courses = serializer.list(user)
        return Response(CourseListSerializer(courses, many=True).data, status=status.HTTP_200_OK)
    if request.method == "POST":
        serializer = CourseListSerializer(data=request.data, context={"user":user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "DELETE":
        serializer = CourseListSerializer()
        serializer.delete()
        return Response({"success":True}, status=status.HTTP_200_OK)


@api_view(['PUT','DELETE'])
@token_auth
def course_action(request, id):
    if request.method == "PUT":
        serializer = CourseActionSerializer(data=request.data, partial=True, context={"id":id})
        if serializer.is_valid():
            serializer.save()
            return Response({"success":True}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        serializer = CourseActionSerializer()
        serializer.delete(id)
        return Response({"success":True}, status=status.HTTP_200_OK)
