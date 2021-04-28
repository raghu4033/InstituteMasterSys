# Generated by Django 3.0 on 2021-03-26 10:49

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AdminArea', '0012_auto_20210325_2222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student_registration',
            name='join_date',
            field=models.DateField(blank=True, default=datetime.datetime(2021, 3, 25, 23, 49, 36, 708548)),
        ),
        migrations.CreateModel(
            name='StudentFees',
            fields=[
                ('installment_no', models.PositiveIntegerField()),
                ('amount', models.PositiveIntegerField(max_length=100)),
                ('payment_date', models.DateField(max_length=8)),
                ('payment_type', models.CharField(max_length=100)),
                ('recipt_no', models.AutoField(primary_key=True, serialize=False)),
                ('fees_invoice', models.FileField(default='', upload_to='FeesInvoice/')),
                ('Student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AdminArea.Student_Registration')),
            ],
        ),
    ]