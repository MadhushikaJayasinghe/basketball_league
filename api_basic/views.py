from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import User, Team, Game, UserTeam
from .serializers import UserSerializer, TeamSerializer, GameSerializer, UserLoginSerializer, \
    UserRegistrationSerializer, TeamRegistrationSerializer, GameRegistrationSerializer, UserTeamSerializer, \
    UserGameSerializer


# This method is used to retrieve all the team list
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_team_list(request):
    teams = Team.objects.all()
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


# This method is used ti retrieve all the game list
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_game_list(request):
    games = Game.objects.all()
    serializer = GameSerializer(games, many=True)
    return Response(serializer.data)


# This method is used to get players in the team
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_players_in_team_list(request, team_id):
    user = request.user
    role = user.role
    if role == 'ADMIN':
        players = User.objects.raw(
            'SELECT*FROM user WHERE role = %s AND email IN (SELECT email FROM user_team WHERE team_id = %s)',
            ['PLAYER', team_id])
        serializer = UserSerializer(players, many=True)
        return Response(serializer.data)
    elif role == 'COACH':
        team = Team.objects.raw('SELECT team_id FROM user_team WHERE email = %s', [user.email,])
        print(team)
        print(int(team_id) == int(team[0].team_id))
        if not team:
            response = {
                'success': False,
                'statusCode': 400,
                'message': 'Coach is not belongs to this team!',

            }
            return Response(response)
        else:
            if int(team_id) == int(team[0].team_id):
                players = User.objects.raw(
                    'SELECT*FROM user WHERE role = %s AND email IN (SELECT email FROM user_team WHERE team_id = %s)',
                    ['PLAYER', team_id])
                print(players)
                serializer = UserSerializer(players, many=True)
                return Response(serializer.data)
            else:
                response = {
                    'success': False,
                    'statusCode': 400,
                    'message': 'Coach is not belongs to this team!',

                }
                return Response(response)
    else:
        response = {
            'success': False,
            'statusCode': 400,
            'message': 'User role PLAYER doesnot have access!',

        }
        return Response(response)


# This method is used to get players who has average score more than 90%
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_best_players_in_team(request, team_id):
    user = request.user
    role = user.role
    if role == 'COACH':
        team = Team.objects.raw('SELECT team_id FROM user_team WHERE email = %s', [user.email,])
        print(team[0])
        print(team_id)
        print(int(team_id) == int(team[0].team_id))
        if not team:
            response = {
                'success': False,
                'statusCode': 400,
                'message': 'User doesnot have a team!',

            }
            return Response(response)
        else:
            if int(team_id) == int(team[0].team_id):
                players = User.objects.raw(
                    'SELECT*FROM user WHERE role = %s AND average_score >= 90 AND email IN (SELECT email FROM '
                    'user_team WHERE team_id = %s)',
                    ['PLAYER', team_id])
                serializer = UserSerializer(players, many=True)
                return Response(serializer.data)
            else:
                response = {
                    'success': False,
                    'statusCode': 400,
                    'message': 'Coach is not belongs to this team!',

                }
                return Response(response)
    else:
        response = {
            'success': False,
            'statusCode': 400,
            'message': 'User role PLAYER and ADMIN doesnot have access!',

        }
        return Response(response)

# This method get players details in a team
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
        team = Team.objects.raw('SELECT team_id FROM user_team WHERE email = %s', [user.email,])
        if not team:
            response = {
                'success': False,
                'statusCode': 400,
                'message': 'User donot have a team team!',

            }
            return Response(response)
        else:
            if int(team_id) == int(team[0].team_id):
                players = User.objects.raw(
                    'SELECT*FROM user WHERE email = %s', [email,])
            else:
                response = {
                    'success': False,
                    'statusCode': 400,
                    'message': 'Coach is not belongs to this team!',

                }
                return Response(response)
    else:
        response = {
            'success': False,
            'statusCode': 400,
            'message': 'User role PLAYER doesnot have access!',

        }
        return Response(response)
    serializer = UserSerializer(players, many=True)
    return Response(serializer.data)


# This method is used to register new users
@api_view(['POST'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
def user_registration(request):
    serializer = UserRegistrationSerializer(data=request.data)
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


# This method is used to generate new access tokens
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


# This method is used to register new teams
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def team_registration(request):
    serializer = TeamRegistrationSerializer(data=request.data)
    valid = serializer.is_valid(raise_exception=True)

    if valid:
        serializer.save()
        status_code = status.HTTP_201_CREATED

        response = {
            'success': True,
            'statusCode': status_code,
            'message': 'Team successfully registered!',
            'user': serializer.data
        }

        return Response(response, status=status_code)


# This method is used to register new games
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def game_registration(request):
    serializer = GameRegistrationSerializer(data=request.data)
    valid = serializer.is_valid(raise_exception=True)

    if valid:
        serializer.save()
        status_code = status.HTTP_201_CREATED

        response = {
            'success': True,
            'statusCode': status_code,
            'message': 'Game successfully registered!',
            'user': serializer.data
        }

        return Response(response, status=status_code)


# This method is used to register new games
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def user_team_registration(request):
    user_id = request.user.id

    serializer = UserTeamSerializer(data=request.data)
    valid = serializer.is_valid(raise_exception=True)

    if valid:
        serializer.save()
        status_code = status.HTTP_201_CREATED

        response = {
            'success': True,
            'statusCode': status_code,
            'message': 'User team successfully registered!',
            'user': serializer.data
        }

        return Response(response, status=status_code)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def user_game_registration(request):
    serializer = UserGameSerializer(data=request.data)
    valid = serializer.is_valid(raise_exception=True)

    if valid:
        serializer.save()
        status_code = status.HTTP_201_CREATED

        response = {
            'success': True,
            'statusCode': status_code,
            'message': 'User game successfully registered!',
            'user': serializer.data
        }

        return Response(response, status=status_code)
