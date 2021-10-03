# Generated by Django 3.1.13 on 2021-10-02 20:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('language', '0004_auto_20211002_1328'),
    ]

    operations = [
        migrations.CreateModel(
            name='LessonData',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('lesson_text', models.CharField(max_length=128)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(null=True)),
                ('taught_language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='language.languagedata')),
            ],
        ),
    ]