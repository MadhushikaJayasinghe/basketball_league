from django.contrib import admin
from .models import User, Team, Game
admin.site.register(User)
admin.site.register(Team)
admin.site.register(Game)
# admin.site.register(UserGame)
# admin.site.register(UserTeam)
# admin.site.register(TeamGame)
