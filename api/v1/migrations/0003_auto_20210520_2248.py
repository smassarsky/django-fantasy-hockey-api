# Generated by Django 3.2.3 on 2021-05-20 22:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_team_city'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='games',
        ),
        migrations.RemoveField(
            model_name='team',
            name='games',
        ),
        migrations.AddField(
            model_name='game',
            name='_teams',
            field=models.ManyToManyField(through='api.GameTeam', to='api.Team'),
        ),
        migrations.AddField(
            model_name='game',
            name='players',
            field=models.ManyToManyField(through='api.GamePlayer', to='api.Player'),
        ),
        migrations.AlterField(
            model_name='gameplayer',
            name='position',
            field=models.CharField(max_length=2),
        ),
        migrations.AlterField(
            model_name='gameteam',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game_teams', to='api.game'),
        ),
        migrations.AlterField(
            model_name='gameteam',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game_teams', to='api.team'),
        ),
    ]