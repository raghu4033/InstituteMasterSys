# Generated by Django 3.0 on 2021-03-31 05:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminArea', '0018_auto_20210329_1955'),
    ]

    operations = [
        migrations.CreateModel(
            name='Submitions_Registration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.CharField(choices=[('Fashion', 'Fashion'), ('Graphics', 'Graphics'), ('FineArt', 'FineArt'), ('Textile', 'Textile'), ('Jwellery', 'Jwellery'), ('All', 'All')], default='all', max_length=200)),
                ('batch', models.CharField(max_length=100)),
                ('subject', models.CharField(max_length=100)),
                ('desc', models.TextField()),
                ('last_date', models.DateField(max_length=8)),
                ('submitions_file', models.FileField(default='', upload_to='NoticeFiles/')),
                ('notice_status', models.CharField(default='active', max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='student_registration',
            name='join_date',
            field=models.DateField(blank=True, default=datetime.datetime(2021, 3, 30, 18, 47, 0, 36490)),
        ),
    ]
