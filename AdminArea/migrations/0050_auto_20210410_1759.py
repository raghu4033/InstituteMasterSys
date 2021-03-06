# Generated by Django 3.0 on 2021-04-10 12:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AdminArea', '0049_student_schedule'),
    ]

    operations = [
        migrations.AddField(
            model_name='student_schedule',
            name='admin_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='AdminArea.Admin_Registration'),
        ),
        migrations.AddField(
            model_name='student_schedule',
            name='faculty_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='AdminArea.Faculty_Registration'),
        ),
    ]
