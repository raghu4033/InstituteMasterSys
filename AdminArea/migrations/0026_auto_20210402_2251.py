# Generated by Django 3.0 on 2021-04-03 09:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminArea', '0025_auto_20210402_0059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notice_registration',
            name='notice_for',
            field=models.CharField(choices=[('fashion', 'fashion'), ('graphics', 'graphics'), ('fineArt', 'fineArt'), ('fextile', 'fextile'), ('jwellery', 'jwellery'), ('All', 'All')], default='all', max_length=200),
        ),
        migrations.AlterField(
            model_name='student_registration',
            name='join_date',
            field=models.DateField(blank=True, default=datetime.datetime(2021, 4, 2, 22, 51, 53, 663901)),
        ),
    ]
