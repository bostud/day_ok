# Generated by Django 3.1.6 on 2021-02-09 22:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0020_student_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Назва')),
                ('date_created', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Джерела',
                'verbose_name_plural': 'Джерела',
            },
        ),
        migrations.AddField(
            model_name='student',
            name='date_end_studying',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата закінчення навчання'),
        ),
        migrations.AddField(
            model_name='student',
            name='source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='schedule.source', verbose_name='Звідки дізнались про нашу школу?'),
        ),
    ]
