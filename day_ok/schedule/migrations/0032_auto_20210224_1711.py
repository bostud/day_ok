# Generated by Django 3.1.7 on 2021-02-24 15:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0031_auto_20210219_2105'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='class_room',
            new_name='classroom',
        ),
        migrations.RenameField(
            model_name='lessons',
            old_name='class_room',
            new_name='classroom',
        ),
    ]
