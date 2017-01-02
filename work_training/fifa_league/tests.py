"""
tests.py | File that contains tests for fifa_league app
"""
from django.test import TestCase
from .factories import TeamFactory, LeagueFactory, TeamStatFactory, \
    PlayerFactory, MatchFactory


class MatchCreateTestCase(TestCase):
    """
    Test Case for Match create
    - test if Match create properly update statistic for teams
    """

    def setUp(self):
        self.team_stat1 = TeamStatFactory()
        self.team_stat2 = TeamStatFactory()

    def test_team_home_win_statistic(self):
        """
        Test when home team wins the guest team (example 2:1)
        :return:
        """
        MatchFactory(team_home=self.team_stat1,
                     team_guest=self.team_stat2,
                     team_home_goals=2,
                     team_guest_goals=1)
        self.assertEqual(self.team_stat1.points, 3)
        self.assertEqual(self.team_stat2.points, 0)

    def test_team_home_lose_statistic(self):
        """
        Test when home team loses to guest team (example 1:2)
        :return:
        """
        MatchFactory(team_home=self.team_stat1,
                     team_guest=self.team_stat2,
                     team_home_goals=1,
                     team_guest_goals=2)
        self.assertEqual(self.team_stat1.points, 0)
        self.assertEqual(self.team_stat2.points, 3)

    def test_team_draw_statistic(self):
        """
        Test statistic update when home team and guest team
        have equal count of goals (example 1:1)
        :return:
        """
        MatchFactory(team_home=self.team_stat1,
                     team_guest=self.team_stat2,
                     team_home_goals=1,
                     team_guest_goals=1)
        self.assertEqual(self.team_stat1.points, 1)
        self.assertEqual(self.team_stat2.points, 1)

    def test_str(self):
        match = MatchFactory()
        self.assertEqual(match.__str__(), '{} vs {} ({}:{})'
                         .format(match.team_home.team.name,
                                 match.team_guest.team.name,
                                 match.team_home_goals,
                                 match.team_guest_goals))


class LeagueModelCreateTestCase(TestCase):
    def setUp(self):
        self.league = LeagueFactory()

    def test_league_create(self):
        league = self.league

        self.assertEqual(league.__str__(), 'TESTLEAGUE')
        self.assertEqual(league.name, 'TESTLEAGUE')
        self.assertEqual(league.shortcut, 'testleague')


class TeamModelCreateTestCase(TestCase):
    def setUp(self):
        self.team = TeamFactory()

    def test_team_create(self):
        team = self.team

        self.assertEqual(team.__str__(), 'Club: {}'.format(team.name))
        self.assertEqual(team.name, '{}'.format(team.name))
        self.assertEqual(team.shortcut, '{}'.format(team.shortcut))


class TeamStatModelCreateTestCase(TestCase):
    def setUp(self):
        self.teamstat = TeamStatFactory()

    def test_teamstat_create(self):
        teamstat = self.teamstat

        self.assertEqual(teamstat.points, 0)
        self.assertEqual(teamstat.match_count, 0)
        self.assertEqual(teamstat.wins, 0)
        self.assertEqual(teamstat.loses, 0)
        self.assertEqual(teamstat.draws, 0)
        self.assertEqual(teamstat.goals_scored, 0)
        self.assertEqual(teamstat.goals_conceded, 0)


class PlayerModelCreateTestCase(TestCase):
    def setUp(self):
        self.player = PlayerFactory()

    def test_player_create(self):
        player = self.player
        self.assertEqual(player.name, 'Rocko Pocko')
        self.assertEqual(player.age, 21)

    def test_player_str(self):
        self.assertEqual(self.player.__str__(), '{} | Club: {}'
                         .format(self.player.name, self.player.team.name))


