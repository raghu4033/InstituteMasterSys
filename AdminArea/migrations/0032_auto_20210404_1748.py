# Generated by Django 3.0 on 2021-04-04 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminArea', '0031_auto_20210404_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student_registration',
            name='last_login',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
