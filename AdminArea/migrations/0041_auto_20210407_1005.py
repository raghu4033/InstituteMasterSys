# Generated by Django 3.0 on 2021-04-07 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminArea', '0040_auto_20210405_2146'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='admin_registration',
            name='id',
        ),
        migrations.AlterField(
            model_name='admin_registration',
            name='email',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
    ]
