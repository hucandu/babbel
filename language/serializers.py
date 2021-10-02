from rest_framework import serializers
from .models import LanguageData
from datetime import datetime
from django.db import connection
from django.db import IntegrityError

class LanguageListSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=100)
    code = serializers.CharField(max_length=100)
    deleted = serializers.DateTimeField(required=False)
    created_at = serializers.DateTimeField(required=False)
    updated_at = serializers.DateTimeField(required=False)

    class Meta:
        read_only_fields = ('id', 'deleted', 'created_at')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        insert_query_build = '''
                INSERT INTO language_languagedata
                (name, code, created_at, updated_at)
                VALUES (%s, %s, %s, %s) RETURNING id;
                '''
        validated_data["created_at"] = datetime.now()
        validated_data["updated_at"] = datetime.now()
        with connection.cursor() as cursor:
            try:
                cursor.execute(insert_query_build, [
                    validated_data.get("name"),
                    validated_data.get("code"),
                    datetime.now(),
                    datetime.now(),
                    ])
                row = cursor.fetchone()
                validated_data["id"] = row[0]
            except IntegrityError as e:
                raise serializers.ValidationError("language code already exists")
            except Exception as e:
                import pdb;pdb.set_trace()
                raise serializers.ValidationError("Error creating data")
        return validated_data


    def list(self):
        select_query_build = '''
                SELECT * FROM language_languagedata
                WHERE deleted IS NULL
                '''
        try:
            rows = LanguageData.objects.raw(select_query_build)
        except Exception as e:
            raise serializers.ValidationError("Error retrieving data")
        return [item for item in rows]


    def delete(self):
        query_build = '''
                UPDATE language_languagedata
                SET deleted = CURRENT_TIMESTAMP
                '''
        with connection.cursor() as cursor:
            try:
                cursor.execute(query_build)
            except Exception as e:
                import pdb;pdb.set_trace()
                raise serializers.ValidationError("Error deleting data")




class LanguageActionSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=100)
    code = serializers.CharField(max_length=100)
    deleted = serializers.DateTimeField(required=False)
    created_at = serializers.CharField(max_length=100, required=False)
    updated_at = serializers.CharField(max_length=100, required=False)

    class Meta:
        read_only_fields = ('id', 'deleted', 'created_at')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        update_query_build = '''
                UPDATE language_languagedata
                SET name = %s,
                code = %s,
                updated_at = %s
                WHERE id = %s;
                '''
        validated_data["updated_at"] = datetime.now()
        if self.partial==True:
            try:
                rows = LanguageData.objects.raw("SELECT * FROM language_languagedata WHERE id=%s", [self.context.get('id')])
                row_data = rows[0].__dict__
                validated_data = {key:validated_data.get(key, row_data.get(key)) for key,value in row_data.items()}
            except Exception as e:
                raise serializers.ValidationError("Error updating data")
        with connection.cursor() as cursor:
            try:
                cursor.execute(update_query_build, [
                    validated_data.get("name"),
                    validated_data.get("code"),
                    datetime.now(),
                    self.context["id"]
                    ])
            except Exception as e:
                raise serializers.ValidationError("Error updating data")
        return validated_data


    def delete(self, id):
        query_build = '''
                UPDATE language_languagedata
                SET deleted = CURRENT_TIMESTAMP
                where id = %s
                '''
        with connection.cursor() as cursor:
            try:
                cursor.execute(query_build, [id])
            except Exception as e:
                raise serializers.ValidationError("Error deleting data")
