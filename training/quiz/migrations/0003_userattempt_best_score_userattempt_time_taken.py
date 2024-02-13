# Generated by Django 5.0.1 on 2024-02-12 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_quiz_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='userattempt',
            name='best_score',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userattempt',
            name='time_taken',
            field=models.TimeField(default='00:00:00'),
        ),
    ]
