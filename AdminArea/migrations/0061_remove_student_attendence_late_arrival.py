# Generated by Django 3.0 on 2021-06-08 05:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AdminArea', '0060_auto_20210606_1220'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student_attendence',
            name='late_arrival',
        ),
    ]
