from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import TeamViewSet, GameViewSet, PlayerViewSet

router = DefaultRouter()

router.register(r'teams', TeamViewSet)
router.register(r'players', PlayerViewSet)
router.register(r'games', GameViewSet)

urlpatterns = router.urls