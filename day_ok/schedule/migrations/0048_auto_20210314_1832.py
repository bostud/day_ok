# Generated by Django 3.1.7 on 2021-03-14 16:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0047_auto_20210314_1831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoicepayment',
            name='invoice',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='schedule.invoice'),
        ),
    ]
