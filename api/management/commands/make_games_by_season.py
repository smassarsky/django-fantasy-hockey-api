import requests
from django.core.management.base import BaseCommand
from api.management.commands.build_game import build_game

# 1 = Y1 | 2 = Y2
# format 11112222
def fetch_games(season):
	url = f"https://statsapi.web.nhl.com/api/v1/schedule?season={season}"
	response = requests.get(url, headers={'Content-Type': 'application/json'})
	if response.status_code != 200:
		print('Invalid Request - Date format is YYYY-MM-DD')
	else:
		games_dict = response.json()
		for date in games_dict['dates']:
			for game in date['games']:
				build_game(game)


class Command(BaseCommand):

	def add_arguments(self, parser):
		parser.add_argument('--season', type=str)

	def handle(self, *args, **options):
		fetch_games(options['season'])