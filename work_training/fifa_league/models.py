from django.db import models


# League main model
class League(models.Model):
    name = models.CharField(max_length=250)
    shortcut = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# Team model, relation for each League
class Team(models.Model):
    name = models.CharField(max_length=250)
    shortcut = models.CharField(max_length=50)

    def __str__(self):
        return "Club: " + self.name


class TeamStat(models.Model):
    league = models.ForeignKey(League, related_name="league")
    team = models.ForeignKey(Team, related_name="team")
    match_count = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    loses = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    goals_scored = models.IntegerField(default=0)
    goals_conceded = models.IntegerField(default=0)
    points = models.IntegerField(default=0)

    def __str__(self):
        return "Stat: " + self.team.name + " in " + self.league.name + " league"


# Player model, relation for each Team
class Player(models.Model):
    team = models.ForeignKey(Team)
    name = models.CharField(max_length=500)
    age = models.IntegerField(default=0)

    def __str__(self):
        return self.name + " | Club: " + self.team.name


class Match(models.Model):
    team_home = models.ForeignKey(TeamStat, related_name="team_home")
    team_guest = models.ForeignKey(TeamStat, related_name="team_guest")
    team_home_goals = models.IntegerField(default=0)
    team_guest_goals = models.IntegerField(default=0)

    def __str__(self):
        return self.team_home.team.name + ' vs ' + self.team_guest.team.name + ' (' + str(self.team_home_goals) + ":" + str(self.team_guest_goals) + ')'
