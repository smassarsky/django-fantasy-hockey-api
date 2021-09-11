from api.v1.utils import get_score_from_game
from django.db.models.base import Model
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from .models import Assist, Game, GameTeam, GamePlayer, Goal, Player, Team
from rest_framework.serializers import ModelSerializer, RelatedField


class TeamSerializer(ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class MiniTeamSerializer(ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name']


class PlayerSerializer(ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'name']


class GamePlayerSerializer(ModelSerializer):
    player = PlayerSerializer()

    class Meta:
        model = GamePlayer
        fields = ['player', 'position', 'jersey_num']

class RetrieveGameTeamSerializer(ModelSerializer):
    roster = SerializerMethodField()
    team = TeamSerializer()

    class Meta:
        model = GameTeam
        fields = ['home_away', 'team', 'roster']

    def get_roster(self, obj):
        return GamePlayerSerializer(obj.get_roster(), many=True).data


class ListGameSerializer(ModelSerializer):
    score = SerializerMethodField()

    class Meta:
        model = Game
        fields = ['id', 'datetime', 'game_type', 'season', 'status', 'score']

    def get_score(self, obj):
        return get_score_from_game(obj)


class RetrieveGameSerializer(ModelSerializer):
    teams = SerializerMethodField()
    events = SerializerMethodField()
    score = SerializerMethodField()

    class Meta:
        model = Game
        fields = ['id', 'api_id', 'datetime', 'game_type', 'season', 'status', 'score', 'events', 'teams']

    def get_teams(self, obj):
        return RetrieveGameTeamSerializer(obj.game_teams, many=True).data
    
    def get_events(self, obj):
        return GameGoalSerializer(obj.goals, many=True).data
    
    def get_score(self, obj):
        return get_score_from_game(obj)


class AssistSerializer(ModelSerializer):
    player = PlayerSerializer()    

    class Meta:
        model = Assist
        fields = ['id', 'player']


class GameGoalSerializer(ModelSerializer):
    team = MiniTeamSerializer()
    player = PlayerSerializer()
    assists = AssistSerializer(many=True)

    class Meta:
        model = Goal
        fields = ['id', 'period', 'time', 'video_url', 'team', 'player', 'assists']


class GoalSerializer(ModelSerializer):
    class Meta:
        model = Goal
        fields = '__all__'

