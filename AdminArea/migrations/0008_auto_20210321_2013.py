# Generated by Django 3.0 on 2021-03-22 07:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminArea', '0007_auto_20210319_0229'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin_Registration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=100)),
                ('mname', models.CharField(max_length=100)),
                ('lname', models.CharField(max_length=100)),
                ('dob', models.DateField(max_length=8)),
                ('gender', models.CharField(choices=[('male', 'male'), ('female', 'female')], default='', max_length=10)),
                ('aadhar', models.CharField(max_length=12)),
                ('address', models.TextField()),
                ('city', models.CharField(max_length=100)),
                ('pin', models.CharField(max_length=10)),
                ('mobile', models.CharField(max_length=10)),
                ('photo', models.ImageField(default='', upload_to='StudentPhotos/')),
                ('status', models.CharField(default='Panding', max_length=100)),
                ('last_login', models.CharField(default='', max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('password', models.CharField(default='', max_length=100)),
                ('cpassword', models.CharField(default='', max_length=100)),
                ('sreenpin', models.CharField(default='', max_length=100)),
                ('csreenpin', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='student_registration',
            name='join_date',
            field=models.DateField(blank=True, default=datetime.datetime(2021, 3, 21, 20, 13, 33, 966913)),
        ),
    ]
