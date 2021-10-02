from django.db import models

# Create your models here.

class UserData(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    profile_picture = models.CharField(max_length=128)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['username', 'deleted']]

class Token(models.Model):
    key = models.CharField(max_length=128)
    user = models.ForeignKey(UserData, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
