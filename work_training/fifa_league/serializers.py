"""
Serializer file | Contains serializers class for Django REST API framework
"""
from rest_framework import serializers
from .models import League


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
