# Generated by Django 3.1.7 on 2021-03-14 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0045_auto_20210314_1639'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoicestatuschangelog',
            name='comment',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
