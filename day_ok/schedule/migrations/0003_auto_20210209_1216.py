# Generated by Django 3.1.6 on 2021-02-09 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0002_auto_20210209_1214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroom',
            name='description',
            field=models.TextField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='classroom',
            name='places_count',
            field=models.IntegerField(null=True),
        ),
    ]
