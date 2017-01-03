"""
tests.py | File that contains tests for fifa_league app
"""
from django.test import TestCase, Client
from .factories import TeamFactory, LeagueFactory, TeamStatFactory, \
    PlayerFactory, MatchFactory
from .serializers import LeagueSerializer, TeamSerializer
from .models import League, Team, Player, TeamStat


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
        self.assertEqual(self.league.__str__(), 'TESTLEAGUE')
        self.assertEqual(self.league.name, 'TESTLEAGUE')
        self.assertEqual(self.league.shortcut, 'testleague')


class TeamModelCreateTestCase(TestCase):
    def setUp(self):
        self.team = TeamFactory()

    def test_team_create(self):
        self.assertEqual(self.team.__str__(), 'Club: {}'
                         .format(self.team.name))
        self.assertEqual(self.team.name, '{}'.format(self.team.name))
        self.assertEqual(self.team.shortcut, '{}'.format(self.team.shortcut))


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


class SerializersTestCase(TestCase):
    def setUp(self):
        self.league = LeagueFactory()
        self.team = TeamFactory()

    def test_league_serializer(self):
        league = self.league
        serializer = LeagueSerializer(league)
        self.assertEqual(serializer.data,
                         {'name': league.name, 'shortcut': league.shortcut})

    def test_team_serializer(self):
        team = self.team
        serializer = TeamSerializer(team)
        self.assertEqual(serializer.data,
                         {'name': team.name, 'shortcut': team.shortcut})


class APITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.league2 = LeagueFactory(name='TESTLEAGUE2',
                                     shortcut='testleague2')
        self.teamstat1 = TeamStatFactory()
        self.teamstat2 = TeamStatFactory()

    def is_lists_equals(self, valid_list, test_list):
        # length list test
        if len(valid_list) != len(test_list):
            return False

        # JSON keys list test
        valid_list_keys = list(valid_list[0].keys())
        test_list_keys = list(test_list[0].keys())
        for key in valid_list_keys:
            if key not in test_list_keys:
                return False

        # if lists equal test
        if valid_list != test_list:
            return False

        return True

    def test_teams_list(self):
        response = self.client.get('/fifa/api/teams/')

        test_serializers = []

        teams_list = Team.objects.all()
        for team in teams_list:
            test_serializers.append(TeamSerializer(team).data)

        response_data = response.json()

        self.assertTrue(self.is_lists_equals(test_serializers, response_data))

    def test_get_teams_from_league(self):
        league = self.teamstat1.league
        response = self.client.get('/fifa/api/teams/get_teams_from_league/{}/'
                                   .format(league.shortcut))
        test_serializers = []

        teams_list = TeamStat.objects.filter(league__shortcut=league.shortcut)
        for teamstat in teams_list:
            test_serializers.append(TeamSerializer(teamstat.team).data)

        response_data = response.json()
        self.assertTrue(self.is_lists_equals(test_serializers, response_data))

    def test_league_list(self):
        response = self.client.get('/fifa/api/leagues/')
        test_serializers = []

        leagues_list = League.objects.all()
        for league in leagues_list:
            test_serializers.append(LeagueSerializer(league).data)

        response_data = response.json()
        self.assertTrue(self.is_lists_equals(test_serializers, response_data))


class TestCreateLeagueViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_with_valid_data(self):
        response = self.client.post('/fifa/create_league/',
                                    {'name': 'TESTLEAGUE1',
                                     'shortcut': 'testleague1'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'),
                         'League TESTLEAGUE1 is create!')

        league = League.objects.get(name='TESTLEAGUE1', shortcut='testleague1')
        self.assertEqual(league.name, 'TESTLEAGUE1')
        self.assertEqual(league.shortcut, 'testleague1')

    def test_create_with_empty_fields(self):
        response = self.client.post('/fifa/create_league/',
                                    {'name': '',
                                     'shortcut': ''},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'),
                         'Some of the fields are empty!')

    def test_create_two_equal(self):
        self.client.post('/fifa/create_league/',
                         {'name': 'TESTLEAGUE1',
                          'shortcut': 'testleague1'},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        response = self.client.post('/fifa/create_league/',
                                    {'name': 'TESTLEAGUE1',
                                     'shortcut': 'testleagues1'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'),
                         'League TESTLEAGUE1 already exist!')


class TestCreateTeamViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_with_valid_data(self):
        response = self.client.post('/fifa/create_team/',
                                    {'team_name': 'TESTTEAM1',
                                     'team_shortcut': 'testteam1'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'),
                         'Team TESTTEAM1 is created!')

        team = Team.objects.get(name='TESTTEAM1', shortcut='testteam1')
        self.assertEqual(team.name, 'TESTTEAM1')
        self.assertEqual(team.shortcut, 'testteam1')

    def test_create_with_empty_fields(self):
        response = self.client.post('/fifa/create_team/',
                                    {'team_name': '',
                                     'team_shortcut': ''},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'),
                         'Some of the fields are empty!')

    def test_create_two_equal(self):
        self.client.post('/fifa/create_team/',
                         {'team_name': 'TESTTEAM1',
                          'team_shortcut': 'testteam1'},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        response = self.client.post('/fifa/create_team/',
                                    {'team_name': 'TESTTEAM1',
                                     'team_shortcut': 'testteam1'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'),
                         'Team TESTTEAM1 already exist!')


# not all possibilities in test
class TestCreatePlayerViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.team = TeamFactory()

    def test_create_with_valid_data(self):
        response = self.client.post('/fifa/create_player/',
                                    {'player_name': 'TESTPLAYER1',
                                     'player_age': 19,
                                     'player_team': self.team.shortcut},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'),
                         'Player TESTPLAYER1 is created!')

        player = Player.objects.get(name='TESTPLAYER1', team=self.team)
        self.assertEqual(player.name, 'TESTPLAYER1')
        self.assertEqual(player.age, 19)
        self.assertEqual(player.team.name, self.team.name)

    def test_create_with_few_empty_fields(self):
        response = self.client.post('/fifa/create_player/',
                                    {'player_name': '',
                                     'player_age': 0,
                                     'player_team': ''},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'),
                         'Some of the fields are empty!')

    def test_create_age_not_number(self):
        response = self.client.post('/fifa/create_player/',
                                    {'player_name': 'TESTPLAYER1',
                                     'player_age': 'not number',
                                     'player_team': self.team.shortcut},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'),
                         '[!] Please enter number!')

    def test_create_two_equal(self):
        self.client.post('/fifa/create_player/',
                         {'player_name': 'TESTPLAYER1',
                          'player_age': 19,
                          'player_team': self.team.shortcut},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        response = self.client.post('/fifa/create_player/',
                                    {'player_name': 'TESTPLAYER1',
                                     'player_age': 19,
                                     'player_team': self.team.shortcut},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.content.decode('utf-8'),
                         'Player TESTPLAYER1 already exist in {}!'
                         .format(self.team.name))


class TestAddTeamToLeagueViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.team = TeamFactory()
        self.league = LeagueFactory()

    def test_create_with_valid_data(self):
        response = self.client.post('/fifa/add_team_to_league/',
                                    {'team_name': self.team.shortcut,
                                     'league_name': self.league.shortcut},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'),
                         'Team {} now in {}!'.format(self.team.name,
                                                     self.league.name))

    def test_create_with_empty_fields(self):
        response = self.client.post('/fifa/add_team_to_league/',
                                    {'team_name': '',
                                     'league_name': ''},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'),
                         'Some of the fields are empty!')


class TestCreateMatchViewTestCase(TestCase):
    def setUp(self):
        self.league = LeagueFactory()
        self.team_home = TeamStatFactory(league=self.league)
        self.team_guest = TeamStatFactory(league=self.league)

    def test_create_with_valid_data(self):
        response = self.client.post('/fifa/create_match/',
                                    {'league': self.league.shortcut,
                                     'home_team': self.team_home.team.shortcut,
                                     'guest_team': self.team_guest
                                     .team.shortcut,
                                     'home_score': 2,
                                     'guest_score': 1},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'),
                         'Match between {} and {} is created!'
                         .format(self.team_home.team.name,
                                 self.team_guest.team.name))
