# Generated by Django 3.1.6 on 2021-02-09 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroom',
            name='room_type',
            field=models.CharField(choices=[('1', 'індивідуальний'), ('2', 'груповий')], default='2', max_length=2),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='status',
            field=models.CharField(choices=[('1', 'оплачено'), ('2', 'очікуємо оплати'), ('3', 'закрито'), ('4', 'тестове заняття')], max_length=2),
        ),
        migrations.AlterField(
            model_name='lessons',
            name='lessons_type',
            field=models.CharField(choices=[('1', 'індивідуальне'), ('2', 'групове')], max_length=2),
        ),
    ]
