# Generated by Django 3.1.13 on 2021-09-30 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210930_0835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='username',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
