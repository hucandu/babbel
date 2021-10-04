from django.db import models

# Create your models here.
from lesson.models import LessonData
from users.models import UserData

class CourseData(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True)

class LessonInCourse(models.Model):
    course = models.ForeignKey(CourseData, on_delete=models.CASCADE)
    lesson = models.ForeignKey(LessonData, on_delete=models.CASCADE)

class CourseSubscription(models.Model):
    course = models.ForeignKey(CourseData, on_delete=models.CASCADE)
    owner = models.ForeignKey(UserData, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True)
