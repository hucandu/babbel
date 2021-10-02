from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import LanguageListSerializer, LanguageActionSerializer
from rest_framework import status

@api_view(['GET', 'POST', 'DELETE'])
def language_list(request):
    if request.method == "GET":
        serializer = LanguageListSerializer()
        languages = serializer.list()
        return Response(LanguageListSerializer(languages, many=True).data, status=status.HTTP_200_OK)
    if request.method == "POST":
        serializer = LanguageListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "DELETE":
        serializer = LanguageListSerializer()
        serializer.delete()
        return Response({"success":True}, status=status.HTTP_200_OK)


@api_view(['PUT', 'PATCH', 'DELETE'])
def language_action(request, id):
    if request.method == "PUT":
        serializer = LanguageActionSerializer(data=request.data, context={"id":id})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "PATCH":
        serializer = LanguageActionSerializer(data=request.data, context={"id":id}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        serializer = LanguageActionSerializer(data=request.data)
        serializer.delete(id)
        return Response({"success":True}, status=status.HTTP_200_OK)
