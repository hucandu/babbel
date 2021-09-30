import uuid
import bcrypt
from rest_framework import serializers
from .models import UserData
from django.db import connection
from datetime import datetime
from django.db import IntegrityError

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)
    profile_picture = serializers.URLField(max_length=200, min_length=8, allow_blank=False)
    deleted = serializers.BooleanField(default=False)
    created_at = serializers.CharField(max_length=100, required=False)

    class Meta:
        read_only_fields = ('id', 'deleted', 'created_at')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        query_build = '''
                INSERT INTO users_userdata
                (first_name, last_name, username, password, profile_picture, deleted, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
                '''
        validated_data["created_at"] = datetime.now()
        validated_data["password"] = bcrypt.hashpw(validated_data["password"].encode('utf8'), bcrypt.gensalt()).decode('utf8')
        with connection.cursor() as cursor:
            try:
                cursor.execute(query_build, [
                    validated_data.get("first_name"),
                    validated_data.get("last_name"),
                    validated_data.get("username"),
                    validated_data.get("password"),
                    validated_data.get("profile_picture"),
                    validated_data.get("deleted"),
                    validated_data.get("created_at")
                ])
            except IntegrityError as e:
                raise serializers.ValidationError("username already exists")
        return validated_data


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=30)
    token = serializers.CharField(max_length=100, required=False)

    class Meta:
        read_only_fields = ('token')
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'write_only': True},
        }


    def create(self, validated_data):
        user_row = UserData.objects.raw('SELECT * FROM users_userdata WHERE username=%s', [validated_data['username']])
        if len(user_row)<1:
            raise serializers.ValidationError("Username does not exist")
        else:
            user_row = user_row[0]
            if not bcrypt.checkpw(validated_data["password"].encode('utf8'), user_row.password.encode('utf8')):
                raise serializers.ValidationError("Password is incorrect")
            query_build = '''
                    INSERT INTO users_token
                    (key, created, user_id)
                    VALUES (%s, %s, %s);
                    '''
            token = str(uuid.uuid4())
            with connection.cursor() as cursor:
                try:
                    cursor.execute(query_build, [
                        token,
                        datetime.now(),
                        user_row.id,
                    ])
                    validated_data['token'] = token
                except Exception as e:
                    raise serializers.ValidationError("Error logging in")
            return validated_data
