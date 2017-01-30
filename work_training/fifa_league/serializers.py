"""
Serializer file | Contains serializers class for Django REST API framework
"""
from rest_framework import serializers
from .models import League, Team, TeamStat, Match, Player
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class LeagueSerializer(serializers.ModelSerializer):
    """
    Serializer for League model
    """
    pk = serializers.ReadOnlyField()
    author = UserSerializer()

    class Meta:
        """
        Define League model and League fields
        """
        model = League
        fields = ['pk', 'name', 'short_description',
                  'full_description', 'logo', 'author']


class TeamSerializer(serializers.ModelSerializer):
    """
    Serializer for Team model
    """
    pk = serializers.ReadOnlyField()

    class Meta:
        """
        Define Team model and Team name and shortcut
        """
        model = Team
        fields = ['pk', 'name', 'logo', 'description']


class TeamOnlyNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['name']


class TeamOnlyNameLogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['logo', 'name']


class TeamStatSerializer(serializers.ModelSerializer):
    """
    Serializer for TeamStat object
    """
    team = TeamOnlyNameLogoSerializer()
    pk = serializers.ReadOnlyField()

    class Meta:
        """
        Meta class where model and fields are defined
        """
        model = TeamStat
        fields = ['pk', 'league', 'team', 'match_count', 'wins',
                  'loses', 'draws', 'goals_scored', 'goals_conceded', 'points']


class MatchSerializer(serializers.ModelSerializer):
    teamstat_team_home = TeamOnlyNameSerializer(source='team_home.team')
    teamstat_team_guest = TeamOnlyNameSerializer(source='team_guest.team')

    class Meta:
        model = Match
        fields = ['teamstat_team_home', 'teamstat_team_guest',
                  'team_home_goals', 'team_guest_goals']


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['name', 'age', 'photo']
