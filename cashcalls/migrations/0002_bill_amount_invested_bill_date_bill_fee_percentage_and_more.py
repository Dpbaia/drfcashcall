# Generated by Django 4.0.4 on 2022-04-29 12:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashcalls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='amount_invested',
            field=models.FloatField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='bill',
            name='date',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='bill',
            name='fee_percentage',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='bill',
            name='final_fee',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='bill',
            name='investor',
            field=models.CharField(default='Investor 1', max_length=80),
        ),
    ]
