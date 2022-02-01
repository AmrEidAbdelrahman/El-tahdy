# Generated by Django 4.0.1 on 2022-02-01 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_remove_exam_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='profile_pic',
            field=models.ImageField(default='default_pp.jpg', upload_to='profile_pics'),
        ),
        migrations.AlterUniqueTogether(
            name='studentanswer',
            unique_together={('studentexam', 'question')},
        ),
    ]
