from django.db import models
from django.db.models.query_utils import check_rel_lookup_compatibility

class Team(models.Model):
	api_id = models.IntegerField()
	name = models.CharField(max_length=50)
	abbreviation = models.CharField(max_length = 3)
	city = models.CharField(max_length = 20)
	division = models.CharField(max_length = 20)
	conference = models.CharField(max_length = 20)
	website = models.URLField()

	def __str__(self):
		return f"{self.city} {self.name}"

class Game(models.Model):
	_teams = models.ManyToManyField(
		Team,
		through='GameTeam',
		related_name='games'
	)
	players = models.ManyToManyField(
		'Player',
		through='GamePlayer',
		related_name='games'
	)
	api_id = models.IntegerField()
	datetime = models.DateTimeField()
	game_type = models.CharField(max_length = 4)
	season = models.CharField(max_length = 10)
	status = models.CharField(max_length = 10)

	def __str__(self):
		return f"{self.home_team} vs. {self.away_team} - {self.datetime}"

	@property
	def home_team(self):
		try:
			return self.game_teams.get(home_away = 'home').team
		except:
			return None

	@home_team.setter
	def home_team(self, team):
		if self.home_team != team:
			if self.home_team:
				self.game_teams.get(home_away = 'home').delete()
			self.game_teams.create(home_away = 'home', team = team)


	@property
	def away_team(self):
		try:
			return self.game_teams.get(home_away = 'away').team
		except:
			return None

	@away_team.setter
	def away_team(self, team):
		if self.away_team != team:
			if self.away_team:
				self.game_teams.get(home_away = 'away').delete()
			self.game_teams.create(home_away = 'away', team = team)


class GameTeam(models.Model):
	game = models.ForeignKey(
		Game,
		on_delete=models.CASCADE,
		related_name='game_teams'
	)
	team = models.ForeignKey(
		Team,
		on_delete=models.CASCADE,
		related_name='game_teams'
	)
	home_away = models.CharField(max_length = 4)

class Player(models.Model):
	api_id = models.IntegerField()
	name = models.CharField(max_length = 50)

	def __str__(self):
		return f"{self.name}"

class GamePlayer(models.Model):
	game = models.ForeignKey(
		Game,
		on_delete=models.CASCADE
	)
	player = models.ForeignKey(
		Player,
		on_delete=models.CASCADE
	)
	position = models.CharField(max_length = 3)
	jersey_num = models.IntegerField()


class Goal(models.Model):
	assist_players = models.ManyToManyField
	game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='goals')
	player = models.ForeignKey(Player, on_delete=models.CASCADE)
	team = models.ForeignKey(Team, on_delete=models.CASCADE)
	api_id = models.IntegerField()
	time = models.CharField(max_length = 5)
	period = models.CharField(max_length = 4)
	video_id = models.IntegerField()
	video_url = models.URLField()

class Assist(models.Model):
	goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
	player = models.ForeignKey(Player, on_delete=models.CASCADE)