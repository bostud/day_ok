# Generated by Django 3.1.7 on 2021-03-25 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0059_auto_20210324_1503'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentpresence',
            name='participants',
            field=models.ManyToManyField(default=None, to='schedule.Student'),
        ),
        migrations.AlterField(
            model_name='studentpresence',
            name='lessons',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.lessons', unique=True, verbose_name='Заняття'),
        ),
        migrations.AlterUniqueTogether(
            name='studentpresence',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='studentpresence',
            name='is_presence',
        ),
        migrations.RemoveField(
            model_name='studentpresence',
            name='student',
        ),
    ]
