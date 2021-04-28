# Generated by Django 3.0 on 2021-04-22 11:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AdminArea', '0055_auto_20210419_1015'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student_Certificate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.CharField(default='', max_length=10)),
                ('take_date', models.DateField(default='', max_length=8)),
                ('admin_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='AdminArea.Admin_Registration')),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='AdminArea.Student_Registration')),
            ],
        ),
    ]
