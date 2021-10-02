from django.db import models

# Create your models here.

class LanguageData(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True)
