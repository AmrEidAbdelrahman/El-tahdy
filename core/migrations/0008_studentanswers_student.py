# Generated by Django 3.2.9 on 2022-01-17 19:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_studentanswers_studentexam'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentanswers',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.student'),
        ),
    ]
