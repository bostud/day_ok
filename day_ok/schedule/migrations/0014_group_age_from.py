# Generated by Django 3.1.6 on 2021-02-09 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0013_auto_20210209_1453'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='age_from',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
