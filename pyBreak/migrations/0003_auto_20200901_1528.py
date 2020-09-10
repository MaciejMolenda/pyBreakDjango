# Generated by Django 3.1 on 2020-09-01 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pyBreak', '0002_auto_20200901_1525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matches',
            name='Breakpoints_converted_ratio',
            field=models.DecimalField(blank=True, decimal_places=15, max_digits=100, null=True),
        ),
        migrations.AlterField(
            model_name='matches',
            name='Breakpoints_saved_ratio',
            field=models.DecimalField(blank=True, decimal_places=15, max_digits=100, null=True),
        ),
        migrations.AlterField(
            model_name='matches',
            name='First_serve_accuracy',
            field=models.DecimalField(blank=True, decimal_places=15, max_digits=100, null=True),
        ),
        migrations.AlterField(
            model_name='matches',
            name='First_serve_points',
            field=models.DecimalField(blank=True, decimal_places=15, max_digits=100, null=True),
        ),
        migrations.AlterField(
            model_name='matches',
            name='Return_1st_serve_points',
            field=models.DecimalField(blank=True, decimal_places=15, max_digits=100, null=True),
        ),
        migrations.AlterField(
            model_name='matches',
            name='Return_2nd_serve_points',
            field=models.DecimalField(blank=True, decimal_places=15, max_digits=100, null=True),
        ),
        migrations.AlterField(
            model_name='matches',
            name='Return_games_won_ratio',
            field=models.DecimalField(blank=True, decimal_places=15, max_digits=100, null=True),
        ),
        migrations.AlterField(
            model_name='matches',
            name='Second_serve_points',
            field=models.DecimalField(blank=True, decimal_places=15, max_digits=100, null=True),
        ),
        migrations.AlterField(
            model_name='matches',
            name='Service_games_won_ratio',
            field=models.DecimalField(blank=True, decimal_places=15, max_digits=100, null=True),
        ),
        migrations.AlterField(
            model_name='matches',
            name='Total_games_ratio',
            field=models.DecimalField(blank=True, decimal_places=15, max_digits=100, null=True),
        ),
        migrations.AlterField(
            model_name='matches',
            name='Total_points',
            field=models.DecimalField(blank=True, decimal_places=15, max_digits=100, null=True),
        ),
        migrations.AlterField(
            model_name='matches',
            name='Total_return_points',
            field=models.DecimalField(blank=True, decimal_places=15, max_digits=100, null=True),
        ),
        migrations.AlterField(
            model_name='matches',
            name='Total_serve_points_won',
            field=models.DecimalField(blank=True, decimal_places=15, max_digits=100, null=True),
        ),
    ]
