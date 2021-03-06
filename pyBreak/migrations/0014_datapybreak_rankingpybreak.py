# Generated by Django 3.1 on 2020-09-12 10:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pyBreak', '0013_player_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataPyBreak',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PyID', models.CharField(max_length=500)),
                ('Date', models.DateField(blank=True, default=datetime.datetime.now)),
                ('Tournament', models.CharField(max_length=500)),
                ('Round', models.CharField(max_length=500)),
                ('Tournament_level', models.CharField(max_length=500)),
                ('Surface', models.CharField(blank=True, max_length=500)),
                ('Rank', models.IntegerField(default=0)),
                ('Rival_rank', models.IntegerField(default=0)),
                ('Rival_hand', models.CharField(blank=True, max_length=500)),
                ('Rival_name', models.CharField(max_length=500)),
                ('Player_odd', models.FloatField(blank=True, null=True)),
                ('Rival_odd', models.FloatField(blank=True, null=True)),
                ('Result', models.CharField(max_length=500)),
                ('Score', models.CharField(max_length=500)),
                ('Match_completed', models.CharField(max_length=500)),
                ('Aces', models.IntegerField(default=0)),
                ('Double_faults', models.IntegerField(default=0)),
                ('First_serve_accuracy', models.FloatField(blank=True, null=True)),
                ('First_serve_points', models.FloatField(blank=True, null=True)),
                ('Second_serve_points', models.FloatField(blank=True, null=True)),
                ('Total_serve_points_won', models.FloatField(blank=True, null=True)),
                ('Breakpoints_saved', models.IntegerField(default=0)),
                ('Breakpoints_todefend', models.IntegerField(default=0)),
                ('Breakpoints_saved_ratio', models.FloatField(blank=True, null=True)),
                ('Return_1st_serve_points', models.FloatField(blank=True, null=True)),
                ('Return_2nd_serve_points', models.FloatField(blank=True, null=True)),
                ('Total_return_points', models.FloatField(blank=True, null=True)),
                ('Breakpoints_converted', models.IntegerField(default=0)),
                ('Breakpoints_created', models.IntegerField(default=0)),
                ('Breakpoints_converted_ratio', models.FloatField(blank=True, null=True)),
                ('Total_points', models.FloatField(blank=True, null=True)),
                ('Service_games_won', models.CharField(max_length=500)),
                ('Service_games_won_ratio', models.FloatField(blank=True, null=True)),
                ('Return_games_won', models.CharField(max_length=500)),
                ('Return_games_won_ratio', models.FloatField(blank=True, null=True)),
                ('Total_games', models.CharField(max_length=500)),
                ('Total_games_ratio', models.FloatField(blank=True, null=True)),
                ('Sets', models.IntegerField(default=0)),
                ('Tiebreak_played', models.IntegerField(default=0)),
                ('Tiebreak_won', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='RankingPyBreak',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PyID', models.CharField(max_length=500)),
                ('Rank', models.IntegerField(default=0)),
                ('Name', models.CharField(max_length=500)),
            ],
        ),
    ]
