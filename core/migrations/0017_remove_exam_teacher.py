# Generated by Django 4.0.1 on 2022-01-29 22:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_remove_student_create_time_remove_student_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exam',
            name='teacher',
        ),
    ]
