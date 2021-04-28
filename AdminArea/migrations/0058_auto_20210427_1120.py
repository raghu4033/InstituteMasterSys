# Generated by Django 3.0 on 2021-04-27 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminArea', '0057_auto_20210423_1020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institute_detaile',
            name='ins_address',
            field=models.TextField(default='Enter Address'),
        ),
        migrations.AlterField(
            model_name='institute_detaile',
            name='ins_email',
            field=models.CharField(default='Enter Institution Email', max_length=100),
        ),
        migrations.AlterField(
            model_name='institute_detaile',
            name='ins_fb',
            field=models.URLField(blank=True, default='https://www.Instagram.com/'),
        ),
        migrations.AlterField(
            model_name='institute_detaile',
            name='ins_google',
            field=models.URLField(blank=True, default='https://www.google.com/'),
        ),
        migrations.AlterField(
            model_name='institute_detaile',
            name='ins_id',
            field=models.CharField(default='Enter Institute Code', max_length=100),
        ),
        migrations.AlterField(
            model_name='institute_detaile',
            name='ins_insta',
            field=models.URLField(blank=True, default='https://www.facebook.com/'),
        ),
        migrations.AlterField(
            model_name='institute_detaile',
            name='ins_name',
            field=models.CharField(default='Enter Institute Name', max_length=100),
        ),
        migrations.AlterField(
            model_name='institute_detaile',
            name='ins_phone',
            field=models.CharField(default='Enter Institution Phone Number', max_length=12),
        ),
        migrations.AlterField(
            model_name='institute_detaile',
            name='ins_web',
            field=models.URLField(blank=True, default='Enter Web Site URL'),
        ),
    ]