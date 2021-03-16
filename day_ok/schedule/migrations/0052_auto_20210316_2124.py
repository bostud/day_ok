# Generated by Django 3.1.7 on 2021-03-16 19:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0051_auto_20210316_2018'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='subject',
        ),
        migrations.AddField(
            model_name='invoice',
            name='subject',
            field=models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='schedule.subject', verbose_name='Предмет'),
        ),
        migrations.AddField(
            model_name='service',
            name='subjects',
            field=models.ManyToManyField(default=None, to='schedule.Subject', verbose_name='Предмет'),
        ),
    ]