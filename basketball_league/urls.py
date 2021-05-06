"""basketball_league URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from api_basic import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('getAllGames', views.get_game_list, name='games'),
    path('getAllTeams', views.get_team_list, name='teams'),
    path('getPlayersInTeam/<int:team_id>', views.get_players_in_team_list, name='players'),
    path('getBestPlayersInTeam/<int:team_id>', views.get_best_players_in_team, name='players'),
    path('getPlayersDetails/<int:team_id>/<str:email>', views.get_players_details, name='player-details'),
    path('register/', views.user_registration, name='user-register'),
    path('login/', views.user_login, name='user-login'),
    path('addGame/', views.game_registration, name='add-game'),
    path('addTeam/', views.team_registration, name='add-team'),
    path('userTeam/', views.user_team_registration, name='add-user-team'),
    path('userGame/', views.user_game_registration, name='add-user-team')
]
