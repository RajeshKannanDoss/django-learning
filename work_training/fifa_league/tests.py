"""
tests.py | File that contains tests for fifa_league app
"""
from django.test import TestCase
from .models import Match, League, Team, TeamStat

# imports for Match create test
from django.db.models.signals import post_save
from .functions import add_points_to_teams


class MatchCreateTestCase(TestCase):
    """
    Test Case for Match create
    - test if Match create properly update statistic for teams
    """

    def setUp(self):
        league = League.objects.create(name='TESTCASELEAGUE',
                                       shortcut='testcaseleague')
        team1 = Team.objects.create(name='TESTCASETEAM1',
                                    shortcut='testcaseteam1')
        team2 = Team.objects.create(name='TESTCASETEAM2',
                                    shortcut='testcaseteam2')

        self.team_stat1 = TeamStat.objects.create(league=league, team=team1)
        self.team_stat2 = TeamStat.objects.create(league=league, team=team2)

        post_save.connect(add_points_to_teams, Match)

    def clean_teams_statistic(self):
        """
        Clean teams statistics (set all statistic variables to 0)
        :return:
        """
        statistic_list = [self.team_stat1, self.team_stat2]
        for stat in statistic_list:
            stat.match_count = 0
            stat.wins = 0
            stat.loses = 0
            stat.draws = 0
            stat.goals_scored = 0
            stat.goals_conceded = 0
            stat.points = 0

    def test_team_home_win_statistic(self):
        """
        Test when home team wins the guest team (example 2:1)
        :return:
        """
        Match.objects.create(team_home=self.team_stat1,
                             team_guest=self.team_stat2,
                             team_home_goals=2,
                             team_guest_goals=1)
        self.assertEqual(self.team_stat1.points, 3)
        self.assertEqual(self.team_stat2.points, 0)
        self.clean_teams_statistic()

    def test_team_home_lose_statistic(self):
        """
        Test when home team loses to guest team (example 1:2)
        :return:
        """
        Match.objects.create(team_home=self.team_stat1,
                             team_guest=self.team_stat2,
                             team_home_goals=1,
                             team_guest_goals=2)
        self.assertEqual(self.team_stat1.points, 0)
        self.assertEqual(self.team_stat2.points, 3)
        self.clean_teams_statistic()

    def test_team_draw_statistic(self):
        """
        Test statistic update when home team and guest team
        have equal count of goals (example 1:1)
        :return:
        """
        Match.objects.create(team_home=self.team_stat1,
                             team_guest=self.team_stat2,
                             team_home_goals=1,
                             team_guest_goals=1)
        self.assertEqual(self.team_stat1.points, 1)
        self.assertEqual(self.team_stat2.points, 1)
