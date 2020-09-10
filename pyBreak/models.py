from django.db import models
from datetime import datetime


class Player(models.Model):
    name = models.CharField(max_length=128)
    rank = models.CharField(max_length=5)
    date = models.DateField(default=datetime.now, blank=True)


class Matches(models.Model):
    PyID = models.CharField(max_length=500)
    Date = models.DateField(default=datetime.now, blank=True)
    Tournament = models.CharField(max_length=500)
    Round = models.CharField(max_length=500)
    Tournament_level = models.CharField(max_length=500)
    Surface = models.CharField(max_length=500, blank=True)
    Rank = models.IntegerField(default=0)
    Rival_rank = models.IntegerField(default=0)
    Rival_hand = models.CharField(max_length=500, blank=True)
    Rival_name = models.CharField(max_length=500)
    Result = models.CharField(max_length=500)
    Score = models.CharField(max_length=500)
    Aces = models.IntegerField(default=0)
    Double_faults = models.IntegerField(default=0)
    First_serve_accuracy = models.FloatField(null=True, blank=True)
    First_serve_points = models.FloatField(null=True, blank=True)
    Second_serve_points = models.FloatField(null=True, blank=True)
    Total_serve_points_won = models.FloatField(null=True, blank=True)
    Breakpoints_saved = models.IntegerField(default=0)
    Breakpoints_todefend = models.IntegerField(default=0)
    Breakpoints_saved_ratio = models.FloatField(null=True, blank=True)
    Return_1st_serve_points = models.FloatField(null=True, blank=True)
    Return_2nd_serve_points = models.FloatField(null=True, blank=True)
    Total_return_points = models.FloatField(null=True, blank=True)
    Breakpoints_converted = models.IntegerField(default=0)
    Breakpoints_created = models.IntegerField(default=0)
    Breakpoints_converted_ratio = models.FloatField(null=True, blank=True)
    Total_points = models.FloatField(null=True, blank=True)
    Service_games_won = models.CharField(max_length=500)
    Service_games_won_ratio = models.FloatField(null=True, blank=True)
    Return_games_won = models.CharField(max_length=500)
    Return_games_won_ratio = models.FloatField(null=True, blank=True)
    Total_games = models.CharField(max_length=500)
    Total_games_ratio = models.FloatField(null=True, blank=True)
    Sets = models.IntegerField(default=0)
    Tiebreak_played = models.IntegerField(default=0)
    Tiebreak_won = models.IntegerField(default=0)
    # Startdate = models.DateField(default=False, blank=True, null=True)
    # Finaldate = models.DateField(default=False, blank=True, null=True)

    def __str__(self):
        return f"{self.PyID} vs {self.Rival_name} , {self.Score}"
