# Generated by Django 3.1 on 2020-09-01 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pyBreak', '0006_auto_20200901_1534'),
    ]

    operations = [
        migrations.AddField(
            model_name='matches',
            name='Breakpoints_converted_ratio',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True),
        ),
        migrations.AddField(
            model_name='matches',
            name='Breakpoints_saved_ratio',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True),
        ),
        migrations.AddField(
            model_name='matches',
            name='Return_1st_serve_points',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True),
        ),
        migrations.AddField(
            model_name='matches',
            name='Return_2nd_serve_points',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True),
        ),
        migrations.AddField(
            model_name='matches',
            name='Total_points',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True),
        ),
        migrations.AddField(
            model_name='matches',
            name='Total_return_points',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True),
        ),
    ]
