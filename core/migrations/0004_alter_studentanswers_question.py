# Generated by Django 3.2.9 on 2022-01-17 17:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_studentanswers_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentanswers',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.exam'),
        ),
    ]