# Generated by Django 4.0.4 on 2022-04-29 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_of_fee', models.CharField(choices=[('up', 'Upfront'), ('yr', 'Yearly'), ('mb', 'Membership')], default='Upfront', max_length=10)),
                ('cash_call_status', models.CharField(choices=[('vl', 'Validated'), ('sn', 'Sent'), ('pd', 'Paid'), ('od', 'Overdue')], max_length=10)),
            ],
        ),
    ]