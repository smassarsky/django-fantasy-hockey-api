import requests
from django.core.management.base import BaseCommand
from api.management.commands.build_game import build_game

# format YYYY-MM-DD
def fetch_games(start_date, end_date):
	url = f"https://statsapi.web.nhl.com/api/v1/schedule?startDate={start_date}&endDate={end_date}"
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
		parser.add_argument('--start_date', type=str)
		parser.add_argument('--end_date', type=str)

	def handle(self, *args, **options):
		start_date = options['start_date']
		end_date = options['end_date']
		fetch_games(start_date, end_date)