from django.db import models


class User(models.Model):
    COACH = 'COACH'
    PLAYER = 'PLAYER'
    ADMIN = 'ADMIN'

    ROLE_TYPES = [
        (COACH, 'Coach'),
        (PLAYER, 'Player'),
        (ADMIN, 'Admin'),
    ]
    role = models.CharField(max_length=6, choices=ROLE_TYPES, default=PLAYER, )
    user_id = models.IntegerField()
    user_name = models.CharField(max_length=100)
    height = models.FloatField()
    average_score = models.FloatField()
    no_of_games = models.IntegerField()

    def __str__(self):
        return self.user_name

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
    game_id = models.IntegerField()
    is_done = models.BooleanField(default=False)
    final_score = models.IntegerField(default=0)
    team_a = models.CharField(max_length=100)
    team_b = models.CharField(max_length=100)
    who_won = models.CharField(max_length=100)

    def __str__(self):
        return str(self.game_id)

    class Meta:
        db_table = "game"


class Team(models.Model):
    name = models.CharField(max_length=100)
    team_id = models.IntegerField()

    def __str__(self):
        return str(self.team_id)

    class Meta:
        db_table = "team"


class UserTeam(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE, db_column='team_id')

    class Meta:
        db_table = "user_team"


class UserGame(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    user_score = models.IntegerField()

    class Meta:
        db_table = "user_game"


class TeamGame(models.Model):
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE)
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    team_score = models.IntegerField()

    class Meta:
        db_table = "team_game"
