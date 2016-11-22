# -*- coding: utf-8 -*-
from django.db import models


class League(models.Model):
    """
    League model
    - shortcut field for user-friendly url
    """
    class Meta:
        verbose_name = 'League'
        verbose_name_plural = 'Leagues'

    name = models.CharField(max_length=250)
    shortcut = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Team(models.Model):
    """
    Team model
    - shortcut field for user-friendly url
    """
    class Meta:
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'

    name = models.CharField(max_length=250)
    shortcut = models.CharField(max_length=50)

    def __str__(self):
        return "Club: " + str(self.name)


class TeamStat(models.Model):
    """
    TeamStat model
    - each TeamStat model related to one team and one league
    """
    class Meta:
        verbose_name = 'Teams statistics'

    league = models.ForeignKey(League, related_name="teams_stat")
    team = models.ForeignKey(Team, related_name="leagues_stat")
    match_count = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    loses = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    goals_scored = models.IntegerField(default=0)
    goals_conceded = models.IntegerField(default=0)
    points = models.IntegerField(default=0)

    def __str__(self):
        return "Stat: " + self.team.name + " in " + self.league.name + " league"


class Player(models.Model):
    """
    Player model
    - one player related to one team
    """
    class Meta:
        verbose_name = 'Player'

    team = models.ForeignKey(Team)
    name = models.CharField(max_length=500)
    age = models.IntegerField(default=0)

    def __str__(self):
        return self.name + " | Club: " + self.team.name


class Match(models.Model):
    """
    Match model
    - one match related to two TeamStat (home and guest teams in specific league)
    """
    class Meta:
        verbose_name = 'Match'
        verbose_name_plural = 'Matches'

    team_home = models.ForeignKey(TeamStat, related_name="home_matches")
    team_guest = models.ForeignKey(TeamStat, related_name="guest_matches")
    team_home_goals = models.IntegerField(default=0)
    team_guest_goals = models.IntegerField(default=0)

    def __str__(self):
        return self.team_home.team.name + ' vs ' + self.team_guest.team.name \
               + ' (' + str(self.team_home_goals) + ":" + str(self.team_guest_goals) + ')'
