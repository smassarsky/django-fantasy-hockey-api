from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Team, Game, Player, Goal, Assist
from .serializers import ListGameSerializer, RetrieveGameSerializer, TeamSerializer, PlayerSerializer, GoalSerializer, AssistSerializer
from .pagination import SmallLimitOffsetPagination
from .utils import get_score_from_game

# https://stackoverflow.com/questions/22616973/django-rest-framework-use-different-serializers-in-the-same-modelviewset
class ReadOnlyMultiSerializerViewSet(ReadOnlyModelViewSet):
	serializers = {
		'default': None,
	}

	def get_serializer_class(self):
		return self.serializers.get(self.action, self.serializers['default'])


class TeamViewSet(ReadOnlyModelViewSet):
	queryset = Team.objects.all()
	serializer_class = TeamSerializer
	permission_classes = []

class GameViewSet(ReadOnlyMultiSerializerViewSet):
	queryset = Game.objects.all()
	permission_classes = []
	pagination_class = SmallLimitOffsetPagination
	serializers = {
		'list': ListGameSerializer,
		'retrieve': RetrieveGameSerializer,
		'default': ListGameSerializer
	}


class PlayerViewSet(ReadOnlyModelViewSet):
	queryset = Player.objects.all()
	serializer_class = PlayerSerializer
	permission_classes = []
	filterset_fields = ['name']

# class GoalViewSet(ReadOnlyModelViewSet):
# 	queryset = Goal.objects.all()
# 	serializer_class = GoalSerializer
# 	permission_classes = [IsAuthenticated]
