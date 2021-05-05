from rest_framework.authentication import SessionAuthentication, TokenAuthentication, BasicAuthentication
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import User, Team, Game
from .serializers import UserSerializer, TeamSerializer, GameSerializer, UserLoginSerializer, UserRegistrationSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_team_list(request):
    teams = Team.objects.all()
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_game_list(request):
    games = Game.objects.all()
    serializer = GameSerializer(games, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_players_in_team_list(request, team_id):
    user = request.user
    role = user.role
    players = []
    if role == 'ADMIN':
        players = User.objects.raw(
            'SELECT*FROM user WHERE role = %s AND email IN (SELECT email FROM user_team WHERE team_id = %s)',
            ['PLAYER', team_id])
    if role == 'COACH':
        team = Team.objects.raw('SELECT*FROM team WHERE email = s', user.email)
        if not team:
            raise_exception = True
        else:
            if team.team_id == team_id:
                players = User.objects.raw(
                    'SELECT*FROM user WHERE role = %s AND email IN (SELECT email FROM user_team WHERE team_id = %s)',
                    ['PLAYER', team_id])
    serializer = UserSerializer(players, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_best_players_in_team(request, team_id):
    user = request.user
    role = user.role
    players = []
    if role == 'COACH':
        team = Team.objects.raw('SELECT*FROM team WHERE email = s', user.email)
        if not team:
            raise_exception = True
        else:
            if team.team_id == team_id:
                players = User.objects.raw(
                        'SELECT*FROM user WHERE role = %s AND average_score >= 90 AND email IN (SELECT email FROM '
                        'user_team WHERE team_id = %s)',
                        ['PLAYER', team_id])
    serializer = UserSerializer(players, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_players_details(request, email, team_id):
    user = request.user
    role = user.role
    players = []
    if role == 'ADMIN':
        players = User.objects.raw(
            'SELECT*FROM user WHERE email = %s)', [email])
    elif role == 'COACH':
        team = Team.objects.raw('SELECT*FROM team WHERE email = s', user.email)
        if not team:
            raise_exception = True
        else:
            if team.team_id == team_id:
                players = User.objects.raw(
                    'SELECT*FROM user WHERE email = %s)', [email])
    else:
        raise_exception = True
    serializer = UserSerializer(players, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
def user_registration(request):
    serializer = UserRegistrationSerializer(data=request.data)
    print(request.data)
    valid = serializer.is_valid(raise_exception=True)

    if valid:
        serializer.save()
        status_code = status.HTTP_201_CREATED

        response = {
            'success': True,
            'statusCode': status_code,
            'message': 'User successfully registered!',
            'user': serializer.data
        }

        return Response(response, status=status_code)


@api_view(['POST'])
def user_login(request):
    serializer = UserLoginSerializer(data=request.data)
    valid = serializer.is_valid(raise_exception=True)

    if valid:
        status_code = status.HTTP_200_OK

        response = {
            'success': True,
            'statusCode': status_code,
            'message': 'User logged in successfully',
            'access': serializer.data['access'],
            'refresh': serializer.data['refresh'],
            'authenticatedUser': {
                'email': serializer.data['email'],
                'role': serializer.data['role']
            }
        }

        return Response(response, status=status_code)
