# Generated by Django 3.1.6 on 2021-02-19 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0030_auto_20210219_1901'),
    ]

    operations = [
        migrations.AddField(
            model_name='lessonsparent',
            name='date_from_valid',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lessonsparent',
            name='date_until_valid',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lessonsparent',
            name='weekdays_for_repeating',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
