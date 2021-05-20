from django.db.utils import Error
import requests
from api.models import Team, Game, Player, GameTeam, GamePlayer, Goal, Assist
from django.utils.dateparse import parse_datetime
from django.db import DatabaseError, transaction

BASE_URL = 'https://statsapi.web.nhl.com/api/v1/game'

# f"{BASE_URL}/{game.api_id}/feed/live
# f"{BASE_URL}/{game.api_id}/content

def build_game(game):
    try:
        home_team = Team.objects.get(api_id = game['teams']['home']['team']['id'])
        away_team = Team.objects.get(api_id = game['teams']['away']['team']['id'])
    
    except Team.DoesNotExist:
        print('team does not exists')
        return 0

    else:
        try:
            with transaction.atomic():
                new_game, created = Game.objects.get_or_create(
                    api_id = game['gamePk'],
                    defaults = {
                        'datetime': parse_datetime(game['gameDate']),
                        'game_type': game['gameType'],
                        'season': game['season'],
                        'status': game['status']['abstractGameState'],
                    }
                )
                new_game.home_team = home_team
                new_game.away_team = away_team

                build_game_rosters_and_events(new_game)

        except DatabaseError:
            print(f"game not created {home_team} {away_team} {game['gameDate']}")

        

def build_game_rosters_and_events(game):
    url = f"{BASE_URL}/{game.api_id}/feed/live"
    response = requests.get(url, headers={'Content-type': 'application/json'})
    game_dict = response.json()

    build_roster(game, game.home_team, game_dict['liveData']['boxscore']['teams']['home'])
    build_roster(game, game.away_team, game_dict['liveData']['boxscore']['teams']['away'])

    build_events(game, game_dict['liveData']['plays'])

    add_game_videos(game)






def build_roster(game, team, players_dict):
    for player in players_dict['players'].values():
        build_player(game, team, player)

def build_player(game, team, player_dict):
    if len(player_dict) > 0:
        try:
            player, created = Player.objects.get_or_create(
                api_id = player_dict['person']['id'],
                defaults = {
                    'name': player_dict['person']['fullName']
                }
            )
            build_game_player(game, team, player, player_dict)

        except DatabaseError:
            print(f"Player not created - {player_dict['person']['fullname']}")


def build_game_player(game, team, player, player_dict):
    try:
        gp, created = GamePlayer.objects.get_or_create(
            game = game,
            player = player,
            defaults = {
                'position': player_dict['position']['abbreviation'],
                'jersey_num': int(player_dict['jerseyNumber'])
            }
        )
        gp.team = team
        gp.save()

    except DatabaseError as e:
        print(f"GamePlayer not created - {game} / {player} {e}")


def build_events(game, plays_dict):
    print(plays_dict['scoringPlays'])
    for goal_id in plays_dict['scoringPlays']:
        build_goal(game, plays_dict['allPlays'][goal_id])


def build_goal(game, goal_dict):
    try:
        goal, created = Goal.objects.get_or_create(
            game = game,
            api_id = goal_dict['about']['eventIdx'],
            defaults = {
                'player': Player.objects.get(api_id = goal_dict['players'][0]['player']['id']),
                'team': Team.objects.get(api_id = goal_dict['team']['id']),
                'time': goal_dict['about']['periodTime'],
                'period': goal_dict['about']['ordinalNum'],
                'video_id': goal_dict['about']['eventId']
            }
        )

        for player in goal_dict['players']:
            if player['playerType'] == 'Assist':
                build_assist(goal, player['player']['id'])

    except DatabaseError as e:
        print(f"Goal {goal_dict['about']['eventIdx']} not created - {e}")

def build_assist(goal, player_api_id):
    try:
        Assist.objects.get_or_create(
            goal = goal,
            player = Player.objects.get(api_id = player_api_id)
        )
    
    except DatabaseError as e:
        print(f"Assist not created {e}")

def add_game_videos(game):
    url = f"{BASE_URL}/{game.api_id}/content"
    response = requests.get(url, headers={'Content-type': 'application/json'})
    game_content_dict = response.json()

    event_codes = game.goals.values_list('video_id', flat=True)

    try:
        goals_dict = list(filter(lambda item : item['type'] == 'GOAL',
        game_content_dict['media']['milestones']['items']))
        for possible_goal in goals_dict:
            if int(possible_goal['statsEventId']) in event_codes:
                video = next((x for x in possible_goal['highlight']['playbacks'] if x['name'].startswith('FLASH_1800K')), False)

                if video:
                    goal = game.goals.get(video_id = int(possible_goal['statsEventId']))
                    goal.video_url = video['url']
                    goal.save()

    except KeyError as e:
        print(f"key error - {e}")