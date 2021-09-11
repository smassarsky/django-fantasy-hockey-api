

def get_score_from_game(game):
    from .serializers import MiniTeamSerializer
    data = {
        'home_team': {
            'team': MiniTeamSerializer(game.home_team).data,
            'goals': game.goals.filter(team=game.home_team).count()
        },
        'away_team': {
            'team': MiniTeamSerializer(game.away_team).data,
            'goals': game.goals.filter(team=game.away_team).count()
        }
    }
    return data