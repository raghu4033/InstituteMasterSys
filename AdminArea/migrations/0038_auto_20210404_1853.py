# Generated by Django 3.0 on 2021-04-04 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AdminArea', '0037_auto_20210404_1842'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student_leave',
            name='student_id',
        ),
        migrations.AddField(
            model_name='student_leave',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='AdminArea.Student_Registration'),
        ),
    ]
