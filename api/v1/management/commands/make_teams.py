import requests
from django.core.management.base import BaseCommand
from api.models import Team

def fetch_teams():
	url = 'https://statsapi.web.nhl.com/api/v1/teams'
	response = requests.get(url, headers={'Content-Type': 'application/json'})
	teams_dict = response.json()
	for team in teams_dict['teams']:
		build_team(team)

def build_team(team):
	print(team)
	Team.objects.get_or_create(
		api_id = team['id'],
		defaults={
			'name': team['teamName'],
			'abbreviation': team['abbreviation'],
			'city': team['locationName'],
			'division': team['division']['name'],
			'conference': team['conference']['name'],
			'website': team['officialSiteUrl']
		}
	)


class Command(BaseCommand):
	def handle(self, *args, **options):
		fetch_teams()