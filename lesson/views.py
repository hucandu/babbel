from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import LessonListSerializer, LessonActionSerializer
from rest_framework import status

@api_view(['GET', 'POST', 'DELETE'])
def lesson_list(request):
    if request.method == "GET":
        serializer = LessonListSerializer()
        lessons = serializer.list()
        return Response(LessonListSerializer(lessons, many=True).data, status=status.HTTP_200_OK)
    if request.method == "POST":
        serializer = LessonListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "DELETE":
        serializer = LessonListSerializer()
        serializer.delete()
        return Response({"success":True}, status=status.HTTP_200_OK)


@api_view(['PUT', 'PATCH', 'DELETE'])
def lesson_action(request, id):
    if request.method == "PUT":
        serializer = LessonActionSerializer(data=request.data, partial=True, context={"id":id})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        serializer = LessonActionSerializer()
        serializer.delete(id)
        return Response({"success":True}, status=status.HTTP_200_OK)
