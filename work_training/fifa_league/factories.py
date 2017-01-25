"""
factories.py - file that contains factory classes for tests
"""
import factory
from django.contrib.auth.models import User
from .models import Match, League, Team, TeamStat, Player
from .functions import add_permissions_to_user


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'TESTUSER%d' % n)
    password = '12345678'
    email = 'test_user@mail.com'

    @classmethod
    def _prepare(cls, create, **kwargs):
        password = kwargs.pop('password', None)
        user = super(UserFactory, cls)._prepare(create, **kwargs)
        if password:
            user.set_password(password)
            if create:
                user.save()
                # add DEFAULT PERMISSIONS to user
                add_permissions_to_user(user)
        return user


class LeagueFactory(factory.DjangoModelFactory):
    class Meta:
        model = League

    name = 'TESTLEAGUE'
    shortcut = 'testleague'
    author = factory.SubFactory(UserFactory)


class TeamFactory(factory.DjangoModelFactory):
    class Meta:
        model = Team

    name = factory.Sequence(lambda n: 'TESTTEAM%d' % n)
    shortcut = factory.Sequence(lambda n: 'testteam%d' % n)
    author = factory.SubFactory(UserFactory)
    description = 'Lorem ipsum'


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
    author = factory.SubFactory(UserFactory)
