# Generated by Django 3.1 on 2020-09-01 16:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pyBreak', '0011_auto_20200901_1601'),
    ]

    operations = [
        migrations.AddField(
            model_name='matches',
            name='Date',
            field=models.DateField(blank=True, default=datetime.datetime.now),
        ),
    ]
