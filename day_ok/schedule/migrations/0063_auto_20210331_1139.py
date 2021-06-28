# Generated by Django 3.1.7 on 2021-03-31 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0062_group_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='lessons_font_color',
            field=models.CharField(default='#FBF9F9', max_length=10, verbose_name='Колір тексту занять'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='lessons_color',
            field=models.CharField(default='#269faf', max_length=10, verbose_name='Колір занять'),
        ),
    ]