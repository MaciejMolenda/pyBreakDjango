# Generated by Django 3.1 on 2020-09-01 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Matches',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PyID', models.CharField(max_length=500)),
                ('Date', models.DateField(blank=True, default=False, null=True)),
                ('Tournament', models.CharField(max_length=500)),
                ('Round', models.CharField(max_length=500)),
                ('Tournament_level', models.CharField(max_length=500)),
                ('Surface', models.CharField(blank=True, max_length=500)),
                ('Rank', models.IntegerField(default=0)),
                ('Rival_rank', models.IntegerField(default=0)),
                ('Rival_hand', models.CharField(blank=True, max_length=500)),
                ('Rival_name', models.CharField(max_length=500)),
                ('Result', models.CharField(max_length=500)),
                ('Score', models.CharField(max_length=500)),
                ('Aces', models.IntegerField(default=0)),
                ('Double_faults', models.IntegerField(default=0)),
                ('First_serve_accuracy', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('First_serve_points', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('Second_serve_points', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('Total_serve_points_won', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('Breakpoints_saved', models.IntegerField(default=0)),
                ('Breakpoints_todefend', models.IntegerField(default=0)),
                ('Breakpoints_saved_ratio', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('Return_1st_serve_points', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('Return_2nd_serve_points', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('Total_return_points', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('Breakpoints_converted', models.IntegerField(default=0)),
                ('Breakpoints_created', models.IntegerField(default=0)),
                ('Breakpoints_converted_ratio', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('Total_points', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('Service_games_won', models.CharField(max_length=500)),
                ('Service_games_won_ratio', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('Return_games_won', models.CharField(max_length=500)),
                ('Return_games_won_ratio', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('Total_games', models.CharField(max_length=500)),
                ('Total_games_ratio', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('Sets', models.IntegerField(default=0)),
                ('Tiebreak_played', models.IntegerField(default=0)),
                ('Tiebreak_won', models.IntegerField(default=0)),
                ('Startdate', models.DateField(blank=True, default=False, null=True)),
                ('Finaldate', models.DateField(blank=True, default=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('rank', models.CharField(max_length=5)),
            ],
        ),
    ]
