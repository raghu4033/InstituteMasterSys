# Generated by Django 3.0 on 2021-04-04 12:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('AdminArea', '0032_auto_20210404_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student_registration',
            name='last_login',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
