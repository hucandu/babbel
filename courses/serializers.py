from rest_framework import serializers
from language.models import LanguageData
from .models import CourseData, LessonInCourse
from datetime import datetime
from django.db import connection
from language.serializers import LanguageListSerializer

class CourseListSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=100)
    lessons = serializers.ListField(child=serializers.IntegerField(min_value=1))
    owned_by = serializers.IntegerField(required=False)
    deleted = serializers.DateTimeField(required=False)
    created_at = serializers.DateTimeField(required=False)
    updated_at = serializers.DateTimeField(required=False)

    class Meta:
        read_only_fields = ('id', 'deleted', 'created_at', 'updated_at', 'owned_by')

    def create(self, validated_data):
        with connection.cursor() as cursor:
            try:
                cursor.execute('BEGIN TRANSACTION;')
                cursor.execute('''
                        INSERT INTO courses_coursedata
                        (name, created_at, updated_at)
                        VALUES (%s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP) RETURNING id;
                        ''', [
                    validated_data.get("name")
                    ])
                row = cursor.fetchone()
                validated_data["id"] = row[0]
                for item in validated_data.get("lessons"):
                    cursor.execute('''
                                INSERT INTO courses_lessonincourse
                                (course_id, lesson_id)
                                VALUES (%s, %s);
                            ''', [
                            validated_data["id"],
                            item
                        ])
                cursor.execute('''
                    INSERT INTO courses_coursesubscription
                    (course_id, owner_id, created_at, updated_at)
                    VALUES (%s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                ''', [
                validated_data["id"],
                self.context.get('user').id
                ])
                cursor.execute('COMMIT TRANSACTION;')
            except Exception as e:
                cursor.execute('ROLLBACK TRANSACTION;')
                raise serializers.ValidationError("Error creating data")
        return validated_data


    def list(self, user):
        select_query_build = '''
                SELECT
                c.id, c.name, l.lesson_id, s.owner_id, c.created_at, c.updated_at
                FROM courses_coursedata as c,
                courses_lessonincourse as l,
                courses_coursesubscription as s
                WHERE c.id = l.course_id
                AND c.id = s.course_id
                AND s.owner_id = %s
                AND c.deleted IS NULL;
                '''
        with connection.cursor() as cursor:
            try:
                cursor.execute(select_query_build, [user.id])
                rows = cursor.fetchall()
                response = []
                course_to_row_map = {}
                for row in rows:
                    course_to_row_map[row[0]] = course_to_row_map.get(row[0], [])+[row[2]]

                courses = set(course_to_row_map.keys())
                for row in rows:
                    if row[0] in courses:
                        data={}
                        courses.remove(row[0])
                        data["id"] = row[0]
                        data["name"] = row[1]
                        data["lessons"] = course_to_row_map[row[0]]
                        data["owned_by"] = row[3]
                        data["created_at"] = row[4]
                        data["updated_at"] = row[5]
                        response.append(data)
                return response
            except Exception as e:
                raise serializers.ValidationError("Error getting data")




class CourseActionSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=100)
    lessons = serializers.ListField(child=serializers.IntegerField(min_value=1))
    owned_by = serializers.IntegerField(required=False)
    deleted = serializers.DateTimeField(required=False)
    created_at = serializers.DateTimeField(required=False)
    updated_at = serializers.DateTimeField(required=False)

    class Meta:
        read_only_fields = ('id', 'deleted', 'created_at', 'updated_at', 'owned_by')

    def create(self, validated_data):
        update_query_build = '''
                UPDATE courses_coursedata
                SET name = %s,
                updated_at = CURRENT_TIMESTAMP
                WHERE id = %s;
                '''
        if self.partial==True:
            try:
                row = CourseData.objects.raw("SELECT * FROM courses_coursedata WHERE id=%s", [self.context.get('id')])[0]
                if not validated_data.get("name"):
                    validated_data["name"] = row.name
            except Exception as e:
                raise serializers.ValidationError("Error updating data")
        with connection.cursor() as cursor:
            try:
                cursor.execute(update_query_build, [
                    validated_data.get("name"),
                    self.context["id"]
                    ])
            except Exception as e:
                raise serializers.ValidationError("Error updating data")
        return validated_data


    def delete(self, id):
        query_build = '''
                UPDATE courses_coursedata
                SET deleted = CURRENT_TIMESTAMP
                where id = %s;
                '''
        with connection.cursor() as cursor:
            try:
                cursor.execute(query_build, [id])
            except Exception as e:
                raise serializers.ValidationError("Error deleting data")
