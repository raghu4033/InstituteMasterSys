# Generated by Django 3.0 on 2021-04-10 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminArea', '0048_faculty_leave'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student_Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_date', models.DateField(default='', max_length=8)),
                ('to_date', models.DateField(default='', max_length=8)),
                ('from_time', models.TimeField(default='', max_length=8)),
                ('to_time', models.TimeField(default='', max_length=8)),
                ('subject', models.CharField(default='', max_length=100)),
                ('classtype', models.CharField(choices=[('lab', 'lab'), ('skeching', 'skeching'), ('theory', 'theory'), ('CAD', 'CAD')], default='', max_length=200)),
                ('batch_nm', models.CharField(default='', max_length=100)),
                ('organizer', models.CharField(default='', max_length=100)),
                ('status', models.CharField(default='active', max_length=100)),
            ],
        ),
    ]
