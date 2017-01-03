"""
factories.py - file that contains factory classes for tests
"""
import factory
from .models import Match, League, Team, TeamStat, Player


class LeagueFactory(factory.DjangoModelFactory):
    class Meta:
        model = League

    name = 'TESTLEAGUE'
    shortcut = 'testleague'


class TeamFactory(factory.DjangoModelFactory):
    class Meta:
        model = Team

    name = factory.Sequence(lambda n: 'TESTTEAM%d' % n)
    shortcut = factory.Sequence(lambda n: 'testteam%d' % n)


class TeamStatFactory(factory.DjangoModelFactory):
    class Meta:
        model = TeamStat

    league = factory.SubFactory(LeagueFactory)
    team = factory.SubFactory(TeamFactory)
    match_count = 0
    wins = 0
    loses = 0
    draws = 0
    goals_scored = 0
    goals_conceded = 0
    points = 0


class MatchFactory(factory.DjangoModelFactory):
    class Meta:
        model = Match

    team_home = factory.SubFactory(TeamStatFactory)
    team_guest = factory.SubFactory(TeamStatFactory)
    team_home_goals = 0
    team_guest_goals = 0


class PlayerFactory(factory.DjangoModelFactory):
    class Meta:
        model = Player

    team = factory.SubFactory(TeamFactory)
    name = 'Rocko Pocko'
    age = 21
