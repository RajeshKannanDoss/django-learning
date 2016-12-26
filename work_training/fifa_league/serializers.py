"""
Serializer file | Contains serializers class for Django REST API framework
"""
from rest_framework import serializers
from .models import League, Team, TeamStat


class LeagueSerializer(serializers.ModelSerializer):
    """
    Serializer for League model
    """
    class Meta:
        """
        Define League model and League fields
        """
        model = League
        fields = ('name', 'shortcut')


class TeamSerializer(serializers.ModelSerializer):
    """
    Serializer for Team model
    """
    class Meta:
        """
        Define Team model and Team name and shortcut
        """
        model = Team
        fields = ('name', 'shortcut')
