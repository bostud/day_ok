# Generated by Django 3.2 on 2021-04-20 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0066_auto_20210421_0043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='phone_number',
            field=models.CharField(max_length=13, null=True, verbose_name='Номер телефону'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='phone_number',
            field=models.CharField(max_length=13, null=True, verbose_name='Номер телефону'),
        ),
    ]
