# Generated by Django 3.0 on 2021-03-27 06:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminArea', '0014_auto_20210326_0048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student_registration',
            name='join_date',
            field=models.DateField(blank=True, default=datetime.datetime(2021, 3, 26, 19, 40, 45, 766091)),
        ),
    ]
