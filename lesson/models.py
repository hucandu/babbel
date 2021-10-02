from django.db import models

# Create your models here.
from language.models import LanguageData

class LessonData(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    taught_language = models.ForeignKey(LanguageData, on_delete=models.CASCADE)
    lesson_text = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True)
