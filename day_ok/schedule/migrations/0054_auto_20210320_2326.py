# Generated by Django 3.1.7 on 2021-03-20 21:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0053_auto_20210319_1703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='source',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='schedule.source', verbose_name='Звідки дізнались про нашу школу?'),
        ),
    ]
