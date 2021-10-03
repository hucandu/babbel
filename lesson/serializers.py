from rest_framework import serializers
from language.models import LanguageData
from.models import LessonData
from datetime import datetime
from django.db import connection
from language.serializers import LanguageListSerializer

class LessonListSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=100)
    taught_language =  LanguageListSerializer(required=False)
    taught_language_id = serializers.IntegerField()
    lesson_text = serializers.CharField(max_length=100)
    deleted = serializers.DateTimeField(required=False)
    created_at = serializers.DateTimeField(required=False)
    updated_at = serializers.DateTimeField(required=False)

    class Meta:
        read_only_fields = ('id', 'deleted', 'created_at', 'updated_at', 'taught_language')
        extra_kwargs = {
            'taught_language_id': {'write_only': True}
        }

    def create(self, validated_data):
        insert_query_build = '''
                INSERT INTO lesson_lessondata
                (name, taught_language_id, lesson_text, created_at, updated_at)
                VALUES (%s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP) RETURNING id;
                '''
        with connection.cursor() as cursor:
            try:
                cursor.execute(insert_query_build, [
                    validated_data.get("name"),
                    validated_data.get("taught_language_id"),
                    validated_data.get("lesson_text"),
                    ])
                row = cursor.fetchone()
                validated_data["id"] = row[0]
            except Exception as e:
                import pdb;pdb.set_trace()
                raise serializers.ValidationError("Error creating data")
        return validated_data


    def list(self):
        select_query_build = '''
                SELECT le.id, le.name,
                    le.lesson_text, le.created_at,
                    le.updated_at, la.name as lesson_name,
                    la.code as lesson_code
                FROM lesson_lessondata AS le, language_languagedata AS la
                WHERE la.id = le.taught_language_id
                AND le.deleted IS NULL;
                '''
        with connection.cursor() as cursor:
            try:
                cursor.execute(select_query_build)
                rows = cursor.fetchall()
                response = []
                for row in rows:
                    obj = LessonData()
                    obj.id = row[0]
                    obj.name = row[1]
                    obj.lesson_text = row[2]
                    obj.created_at = row[3]
                    obj.updated_at = row[4]
                    obj.taught_language = LanguageData()
                    obj.taught_language.name = row[5]
                    obj.taught_language.code = row[6]
                    response.append(obj)
                return response
            except Exception as e:
                import pdb;pdb.set_trace()
                raise serializers.ValidationError("Error creating data")




class LessonActionSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=100)
    taught_language =  LanguageListSerializer(required=False)
    taught_language_id = serializers.IntegerField()
    lesson_text = serializers.CharField(max_length=100)
    deleted = serializers.DateTimeField(required=False)
    created_at = serializers.DateTimeField(required=False)
    updated_at = serializers.DateTimeField(required=False)

    class Meta:
        read_only_fields = ('id', 'deleted', 'created_at', 'updated_at', 'taught_language')
        extra_kwargs = {
            'taught_language_id': {'write_only': True}
        }

    def create(self, validated_data):
        update_query_build = '''
                UPDATE lesson_lessondata
                SET name = %s,
                taught_language_id = %s,
                lesson_text =%s,
                updated_at = CURRENT_TIMESTAMP
                WHERE id = %s;
                '''
        if self.partial==True:
            try:
                rows = LanguageData.objects.raw("SELECT * FROM lesson_lessondata WHERE id=%s", [self.context.get('id')])
                row_data = rows[0].__dict__
                validated_data = {key:validated_data.get(key, row_data.get(key)) for key,value in row_data.items()}
            except Exception as e:
                raise serializers.ValidationError("Error updating data")
        with connection.cursor() as cursor:
            try:
                cursor.execute(update_query_build, [
                    validated_data.get("name"),
                    validated_data.get("taught_language_id"),
                    validated_data.get("lesson_text"),
                    self.context["id"]
                    ])
            except Exception as e:
                raise serializers.ValidationError("Error updating data")
        return validated_data


    def delete(self, id):
        query_build = '''
                UPDATE lesson_lessondata
                SET deleted = CURRENT_TIMESTAMP
                where id = %s
                '''
        with connection.cursor() as cursor:
            try:
                cursor.execute(query_build, [id])
            except Exception as e:
                raise serializers.ValidationError("Error deleting data")
