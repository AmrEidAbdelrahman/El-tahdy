# Generated by Django 3.2.9 on 2022-01-17 19:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_studentanswers_student'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentanswers',
            name='student',
        ),
    ]
