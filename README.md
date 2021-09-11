## Django / DRF API for Fantasy Hockey application

Pulls team and game data from the NHL's stats API

Eventually will allow users to create a matchup with friends where they can pick players from a team over the course of the matchup.  The user with the most points at the end of the matchup wins.


#### Instructions

Create virtual environment in application root directory.  Activate environtment.  Install packages:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run migrations:

`python manage.py migrate`

Pull team data from the NHL's API:

`python manage.py make_teams`

Pull game data from NHL API:

`python manage.py make_games_by_date_range --start_date YYYY-MM-DD --end_date YYYY-MM-DD`

OR

Y=Year1, Z=Year2

`python manage.py make_games_by_season --season YYYYZZZZ`