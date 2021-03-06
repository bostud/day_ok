# Generated by Django 3.1.6 on 2021-02-09 15:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0017_teacher_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='students',
            field=models.ManyToManyField(blank=True, null=True, to='schedule.Student', verbose_name='Учні'),
        ),
        migrations.AlterField(
            model_name='group',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='schedule.subject', verbose_name='Предмет'),
        ),
        migrations.AlterField(
            model_name='group',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='schedule.teacher', verbose_name='Викладач'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='subjects',
            field=models.ManyToManyField(blank=True, null=True, to='schedule.Subject', verbose_name='Предмети'),
        ),
    ]
