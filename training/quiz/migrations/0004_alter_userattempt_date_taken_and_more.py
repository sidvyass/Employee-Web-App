# Generated by Django 5.0.1 on 2024-02-13 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_userattempt_best_score_userattempt_time_taken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userattempt',
            name='date_taken',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date Taken'),
        ),
        migrations.AlterField(
            model_name='userattempt',
            name='time_taken',
            field=models.IntegerField(default=0),
        ),
    ]
