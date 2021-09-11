from django.db.models.base import Model
from .models import Assist, Game, Goal, Player, Team
from rest_framework.serializers import ModelSerializer

class TeamSerializer(ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

class GameSerializer(ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'

class PlayerSerializer(ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'

class GoalSerializer(ModelSerializer):
    class Meta:
        model = Goal
        fields = '__all__'

class AssistSerializer(ModelSerializer):
    class Meta:
        model = Assist
        fields = '__all__'