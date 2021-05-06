from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from api_basic.managers import CustomUserManager


class Team(models.Model):
    name = models.CharField(max_length=100)
    team_id = models.AutoField(primary_key=True)

    def __str__(self):
        return str(self.team_id)

    class Meta:
        db_table = "team"


class User(AbstractBaseUser, PermissionsMixin):
    COACH = 'COACH'
    PLAYER = 'PLAYER'
    ADMIN = 'ADMIN'

    ROLE_TYPES = [
        (COACH, 'Coach'),
        (PLAYER, 'Player'),
        (ADMIN, 'Admin'),
    ]
    role = models.CharField(max_length=6, choices=ROLE_TYPES, default=PLAYER, )
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    height = models.FloatField(default=0)
    average_score = models.FloatField(default=0)
    no_of_games = models.IntegerField(default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        db_table = "user"


class Game(models.Model):
    SG = 'SG'
    QF = 'QF'
    SF = 'SF'
    FI = 'FI'

    GAME_TYPES = [
        (SG, 'Selection Game'),
        (QF, 'Quarter Final'),
        (SF, 'Semi Final'),
        (FI, 'Final')
    ]
    game = models.CharField(max_length=6, choices=GAME_TYPES, default=SG, )
    game_id = models.AutoField(primary_key=True)
    is_done = models.BooleanField(default=False)
    team_id = models.ManyToManyField(Team)
    team_score = models.IntegerField(default=0)

    def __str__(self):
        return str(self.game_id)

    class Meta:
        db_table = "game"


class UserTeam(models.Model):
    email = models.EmailField()
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE, db_column='team_id')

    class Meta:
        db_table = "user_team"


class UserGame(models.Model):
    email = models.EmailField()
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    user_score = models.IntegerField(default=0)

    class Meta:
        db_table = "user_game"


# class TeamGame(models.Model):
#     team_id = models.ForeignKey(Team, on_delete=models.CASCADE)
#     game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
#     team_score = models.IntegerField()
#
#     class Meta:
#         db_table = "team_game"


class UserStat(models.Model):
    email = models.ForeignKey(User, on_delete=models.CASCADE)
    is_logged_in = models.BooleanField(default=False)
    login_time = models.DateTimeField(default=timezone.now)
    logout_time = models.DateTimeField()

    def __str__(self):
        return str(self.login_time)
