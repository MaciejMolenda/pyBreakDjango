# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_flag = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class PybreakMatches(models.Model):
    pyid = models.CharField(db_column='PyID', max_length=500)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    tournament = models.CharField(db_column='Tournament', max_length=500)  # Field name made lowercase.
    round = models.CharField(db_column='Round', max_length=500)  # Field name made lowercase.
    tournament_level = models.CharField(db_column='Tournament_level', max_length=500)  # Field name made lowercase.
    surface = models.CharField(db_column='Surface', max_length=500)  # Field name made lowercase.
    rank = models.IntegerField(db_column='Rank')  # Field name made lowercase.
    rival_rank = models.IntegerField(db_column='Rival_rank')  # Field name made lowercase.
    rival_hand = models.CharField(db_column='Rival_hand', max_length=500)  # Field name made lowercase.
    rival_name = models.CharField(db_column='Rival_name', max_length=500)  # Field name made lowercase.
    result = models.CharField(db_column='Result', max_length=500)  # Field name made lowercase.
    score = models.CharField(db_column='Score', max_length=500)  # Field name made lowercase.
    aces = models.IntegerField(db_column='Aces')  # Field name made lowercase.
    double_faults = models.IntegerField(db_column='Double_faults')  # Field name made lowercase.
    first_serve_accuracy = models.DecimalField(db_column='First_serve_accuracy', max_digits=10, decimal_places=5, blank=True, null=True)  # Field name made lowercase. max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    first_serve_points = models.DecimalField(db_column='First_serve_points', max_digits=10, decimal_places=5, blank=True, null=True)  # Field name made lowercase. max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    second_serve_points = models.DecimalField(db_column='Second_serve_points', max_digits=10, decimal_places=5, blank=True, null=True)  # Field name made lowercase. max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    total_serve_points_won = models.DecimalField(db_column='Total_serve_points_won', max_digits=10, decimal_places=5, blank=True, null=True)  # Field name made lowercase. max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    breakpoints_saved = models.IntegerField(db_column='Breakpoints_saved')  # Field name made lowercase.
    breakpoints_todefend = models.IntegerField(db_column='Breakpoints_todefend')  # Field name made lowercase.
    breakpoints_saved_ratio = models.DecimalField(db_column='Breakpoints_saved_ratio', max_digits=10, decimal_places=5, blank=True, null=True)  # Field name made lowercase. max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    return_1st_serve_points = models.DecimalField(db_column='Return_1st_serve_points', max_digits=10, decimal_places=5, blank=True, null=True)  # Field name made lowercase. max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    return_2nd_serve_points = models.DecimalField(db_column='Return_2nd_serve_points', max_digits=10, decimal_places=5, blank=True, null=True)  # Field name made lowercase. max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    total_return_points = models.DecimalField(db_column='Total_return_points', max_digits=10, decimal_places=5, blank=True, null=True)  # Field name made lowercase. max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    breakpoints_converted = models.IntegerField(db_column='Breakpoints_converted')  # Field name made lowercase.
    breakpoints_created = models.IntegerField(db_column='Breakpoints_created')  # Field name made lowercase.
    breakpoints_converted_ratio = models.DecimalField(db_column='Breakpoints_converted_ratio', max_digits=10, decimal_places=5, blank=True, null=True)  # Field name made lowercase. max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    total_points = models.DecimalField(db_column='Total_points', max_digits=10, decimal_places=5, blank=True, null=True)  # Field name made lowercase. max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    service_games_won = models.CharField(db_column='Service_games_won', max_length=500)  # Field name made lowercase.
    service_games_won_ratio = models.DecimalField(db_column='Service_games_won_ratio', max_digits=10, decimal_places=5, blank=True, null=True)  # Field name made lowercase. max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    return_games_won = models.CharField(db_column='Return_games_won', max_length=500)  # Field name made lowercase.
    return_games_won_ratio = models.DecimalField(db_column='Return_games_won_ratio', max_digits=10, decimal_places=5, blank=True, null=True)  # Field name made lowercase. max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    total_games = models.CharField(db_column='Total_games', max_length=500)  # Field name made lowercase.
    total_games_ratio = models.DecimalField(db_column='Total_games_ratio', max_digits=10, decimal_places=5, blank=True, null=True)  # Field name made lowercase. max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    sets = models.IntegerField(db_column='Sets')  # Field name made lowercase.
    tiebreak_played = models.IntegerField(db_column='Tiebreak_played')  # Field name made lowercase.
    tiebreak_won = models.IntegerField(db_column='Tiebreak_won')  # Field name made lowercase.
    startdate = models.DateField(db_column='Startdate', blank=True, null=True)  # Field name made lowercase.
    finaldate = models.DateField(db_column='Finaldate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'pyBreak_matches'


class PybreakPlayer(models.Model):
    name = models.CharField(max_length=128)
    rank = models.CharField(max_length=5)

    class Meta:
        managed = False
        db_table = 'pyBreak_player'
