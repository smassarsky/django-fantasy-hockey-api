from django.db.models import query
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Team, Game, Player, Goal, Assist
from .serializers import TeamSerializer, GameSerializer, PlayerSerializer, GoalSerializer, AssistSerializer


class TeamViewSet(ReadOnlyModelViewSet):
	queryset = Team.objects.all()
	serializer_class = TeamSerializer
	permission_classes = []

class GameViewSet(ReadOnlyModelViewSet):
	queryset = Game.objects.all()
	serializer_class = GameSerializer
	permission_classes = []

class PlayerViewSet(ReadOnlyModelViewSet):
	queryset = Player.objects.all()
	serializer_class = PlayerSerializer
	permission_classes = []
	filterset_fields = ['name']

# class GoalViewSet(ReadOnlyModelViewSet):
# 	queryset = Goal.objects.all()
# 	serializer_class = GoalSerializer
# 	permission_classes = [IsAuthenticated]
