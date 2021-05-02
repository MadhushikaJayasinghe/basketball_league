from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Team, Game, UserGame, UserTeam, TeamGame
from .serializers import UserSerializer, TeamSerializer, GameSerializer
from rest_framework.decorators import api_view


@api_view(['GET'])
def get_team_list(request):
    teams = Team.objects.all()
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_game_list(request):
    games = Game.objects.all()
    serializer = GameSerializer(games, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_players_in_team_list(request, team_id):
    players = User.objects.raw(
        'SELECT*FROM user WHERE role = %s AND user_id IN (SELECT user_id FROM user_team WHERE team_id = %s)',
        ['PLAYER', team_id])
    serializer = UserSerializer(players, many=True)
    return Response(serializer.data)