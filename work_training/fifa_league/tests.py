"""
tests.py | File that contains tests for fifa_league app
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .factories import TeamFactory, LeagueFactory, TeamStatFactory, \
    PlayerFactory, MatchFactory, UserFactory
from .serializers import LeagueSerializer, TeamSerializer, UserSerializer
from .models import League, Team, Player, TeamStat
from django.core.files.uploadedfile import SimpleUploadedFile
import os


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


class TeamModelCreateTestCase(TestCase):
    def setUp(self):
        self.team = TeamFactory()

    def test_team_create(self):
        self.assertEqual(self.team.__str__(), 'Club: {}'
                         .format(self.team.name))
        self.assertEqual(self.team.name, '{}'.format(self.team.name))


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
                         {'name': league.name,
                          'short_description': league.short_description,
                          'full_description': league.full_description,
                          'logo': league.logo.url, 'pk': league.pk,
                          'author': UserSerializer(league.author).data})

    def test_team_serializer(self):
        team = self.team
        serializer = TeamSerializer(team)
        self.assertEqual(serializer.data,
                         {'name': team.name,
                          'description': team.description,
                          'logo': team.logo.url, 'pk': team.pk})


class APITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.league2 = LeagueFactory(name='TESTLEAGUE2')
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
        response = self.client.get('/fifa/api/teams/{}/get_teams_from_league/'
                                   .format(league.pk))
        test_serializers = []

        teams_list = TeamStat.objects.filter(league__pk=league.pk)
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


class TestCreateLeagueTestCase(TestCase):
    def setUp(self):
        self.user_password = '1234'
        self.user = UserFactory(password=self.user_password)
        self.client = Client()
        self.client.login(username=self.user.username,
                          password=self.user_password)

    def test_create_with_valid_data_and_default_logo(self):
        response = self.client.post('/fifa/api/leagues/',
                                    {'name': 'TESTLEAGUE1',
                                     'short_description': 'Lorem',
                                     'full_description': 'Lorem ipsum',
                                     'logo': ''},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'),
                         '"League TESTLEAGUE1 is create!"')

        league = League.objects.get(name='TESTLEAGUE1')
        self.assertEqual(league.name, 'TESTLEAGUE1')
        self.assertEqual(league.short_description, 'Lorem')
        self.assertEqual(league.full_description, 'Lorem ipsum')
        self.assertEqual(league.logo.url, '/media/static/fifa_league'
                                          '/league/default-league-logo.svg')

    def test_create_with_valid_data_and_custom_logo(self):
        main_dir = os.path.dirname(__file__)
        file = open(os.path.join(main_dir,
                                 'test/files/league-custom-logo.svg'), 'rb')
        response = self.client.post('/fifa/api/leagues/',
                                    {'name': 'TESTLEAGUE1',
                                     'short_description': 'Lorem',
                                     'full_description': 'Lorem ipsum',
                                     'logo': SimpleUploadedFile(file.name,
                                                                file.read())},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'),
                         '"League TESTLEAGUE1 is create!"')

        league = League.objects.get(name='TESTLEAGUE1')
        self.assertEqual(league.name, 'TESTLEAGUE1')
        self.assertEqual(league.short_description, 'Lorem')
        self.assertEqual(league.full_description, 'Lorem ipsum')
        try:
            self.assertEqual(league.logo.url, '/media/uploads/leagues/'
                                              'logos/league-custom-logo.svg')
        finally:
            league.logo.storage.delete(league.logo.name)

    def test_create_with_empty_fields(self):
        response = self.client.post('/fifa/api/leagues/',
                                    {'name': '',
                                     'short_description': 'Lorem',
                                     'full_description': 'Lorem ipsum',
                                     'logo': ''},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'),
                         'Please enter correct data!')

    def test_create_two_equal(self):
        self.client.post('/fifa/api/leagues/',
                         {'name': 'TESTLEAGUE1',
                          'short_description': 'Lorem',
                          'full_description': 'Lorem ipsum',
                          'logo': ''},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        response = self.client.post('/fifa/api/leagues/',
                                    {'name': 'TESTLEAGUE1',
                                     'short_description': 'Lorem',
                                     'full_description': 'Lorem ipsum',
                                     'logo': ''},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'),
                         'League TESTLEAGUE1 already exist!')

    def test_unauthenticated_user(self):
        client = Client()
        response = client.post('/fifa/api/leagues/',
                               {'name': 'TESTLEAGUE1',
                                'short_description': 'Lorem',
                                'full_description': 'Lorem ipsum',
                                'logo': ''},
                               HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 403)

    def test_authenticated_user_without_permissions(self):
        client = Client()
        User.objects.create_user(username='testuser', password='12345678')
        client.login(username='testuser', password='12345678')
        response = client.post('/fifa/api/leagues/',
                               {'name': 'TESTLEAGUE1',
                                'short_description': 'Lorem',
                                'full_description': 'Lorem ipsum',
                                'logo': ''},
                               HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 403)


class TestUpdateLeagueTestCase(TestCase):
    def setUp(self):
        self.password = '1234'
        self.user = UserFactory(password=self.password)
        self.anon_client = Client()
        self.auth_client = Client()
        self.auth_client.login(username=self.user.username,
                               password=self.password)

    def _test_update_with_valid_data_and_without_logo_change(self):
        league = LeagueFactory(short_description='Lorem',
                               full_description='Lorem ipsum',
                               author=self.user)
        response = self.auth_client.put('/fifa/api/leagues/{}/'
                                        .format(league.pk),
                                        {'name': 'TESTLEAGUE',
                                         'shortcut': 'testleague',
                                         'short_description': 'Lorem Lorem',
                                         'full_description': 'Lorem ipsum '
                                                             'Lorem ipsum',
                                         'logo': ''},
                                        HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'),
                         '"Object is updated"')

    def _test_update_with_valid_data_and_logo_change(self):
        main_dir = os.path.dirname(__file__)
        file = open(os.path.join(main_dir,
                                 'test/files/league-custom-logo.svg'), 'rb')
        league = LeagueFactory(short_description='Lorem',
                               full_description='Lorem ipsum',
                               author=self.user)
        response = self.auth_client.put('/fifa/api/leagues/{}/'
                                        .format(league.pk),
                                        {'name': 'TESTLEAGUE1',
                                         'shortcut': 'testleague1',
                                         'short_description': 'Lorem Lorem',
                                         'full_description': 'Lorem ipsum '
                                                             'Lorem ipsum',
                                         'logo': SimpleUploadedFile(file.name,
                                                                    file.read()
                                                                    )},
                                        HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'),
                         '"Object is updated"')
        try:
            self.assertEqual(league.logo.url, '/media/uploads/leagues/'
                                              'logos/league-custom-logo.svg')
        finally:
            league.logo.storage.delete(league.logo.name)


class TestCreateTeamTestCase(TestCase):
    def setUp(self):
        self.user_password = '1234'
        self.user = UserFactory(password=self.user_password)
        self.client = Client()
        self.client.login(username=self.user.username,
                          password=self.user_password)

    def test_create_with_valid_data_without_logo(self):
        response = self.client.post('/fifa/api/teams/',
                                    {'name': 'TESTTEAM1',
                                     'description': 'Lorem ipsum',
                                     'logo': ''},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'),
                         '"Team TESTTEAM1 is created!"')

        team = Team.objects.get(name='TESTTEAM1')
        self.assertEqual(team.name, 'TESTTEAM1')
        self.assertEqual(team.description, 'Lorem ipsum')
        self.assertEqual(team.logo.url,
                         '/media/static/fifa_league/'
                         'team/default-team-logo.svg')

    def test_create_with_empty_fields(self):
        response = self.client.post('/fifa/api/teams/',
                                    {'name': '',
                                     'shortcut': '',
                                     'description': '',
                                     'logo': ''},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'),
                         'Please enter correct data!')

    def test_create_two_equal(self):
        self.client.post('/fifa/api/teams/',
                         {'name': 'TESTTEAM1',
                          'shortcut': 'testteam1',
                          'description': 'Lorem ipsum',
                          'logo': ''},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        response = self.client.post('/fifa/api/teams/',
                                    {'name': 'TESTTEAM1',
                                     'shortcut': 'testteam1',
                                     'description': 'Lorem ipsum lorem',
                                     'logo': ''},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'),
                         'Team TESTTEAM1 already exist!')

    def test_unauthenticated_user(self):
        client = Client()
        response = client.post('/fifa/api/teams/',
                               {'name': 'TESTTEAM1',
                                'shortcut': 'testteam1',
                                'description': 'Lorem ipsum',
                                'logo': ''},
                               HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 403)

    def test_authenticated_user_without_permissions(self):
        client = Client()
        User.objects.create_user(username='testuser', password='12345678')
        client.login(username='testuser', password='12345678')
        response = client.post('/fifa/api/teams/',
                               {'name': 'TESTTEAM1',
                                'shortcut': 'testteam1',
                                'description': 'Lorem ipsum',
                                'logo': ''},
                               HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 403)


class TestCreatePlayerTestCase(TestCase):
    def setUp(self):
        self.team = TeamFactory()
        self.user_password = '1234'
        self.user = UserFactory(password=self.user_password)
        self.client = Client()
        self.client.login(username=self.user.username,
                          password=self.user_password)

    def test_create_with_valid_data_with_default_photo(self):
        response = self.client.post('/fifa/api/players/',
                                    {'name': 'TESTPLAYER1',
                                     'age': 19,
                                     'team': self.team.pk,
                                     'photo': ''},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'),
                         '"Player TESTPLAYER1 is created!"')

        player = Player.objects.get(name='TESTPLAYER1', team=self.team)
        self.assertEqual(player.name, 'TESTPLAYER1')
        self.assertEqual(player.age, 19)
        self.assertEqual(player.team.name, self.team.name)
        self.assertEqual(player.photo.url, '/media/static/fifa_league'
                                           '/player/default-player-photo.svg')

    def test_create_with_few_empty_fields(self):
        response = self.client.post('/fifa/api/players/',
                                    {'name': '',
                                     'age': 0,
                                     'team': '',
                                     'photo': ''},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'),
                         'Please enter correct data!')

    def test_create_age_not_number(self):
        response = self.client.post('/fifa/api/players/',
                                    {'name': 'TESTPLAYER1',
                                     'age': 'not number',
                                     'team': self.team.pk,
                                     'photo': ''},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'),
                         'Please enter correct data!')

    def test_create_two_equal(self):
        self.client.post('/fifa/api/players/',
                         {'name': 'TESTPLAYER1',
                          'age': 19,
                          'team': self.team.pk,
                          'photo': ''},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        response = self.client.post('/fifa/api/players/',
                                    {'name': 'TESTPLAYER1',
                                     'age': 19,
                                     'team': self.team.pk,
                                     'photo': ''},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'),
                         'Player TESTPLAYER1 already exist!'
                         .format(self.team.name))

    def test_unauthenticated_user(self):
        client = Client()
        response = client.post('/fifa/api/players/',
                               {'name': 'TESTPLAYER1',
                                'age': 19,
                                'team': self.team.pk,
                                'photo': ''},
                               HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 403)

    def test_authenticated_user_without_permissions(self):
        client = Client()
        User.objects.create_user(username='testuser', password='12345678')
        client.login(username='testuser', password='12345678')
        response = client.post('/fifa/api/players/',
                               {'name': 'TESTPLAYER1',
                                'age': 19,
                                'team': self.team.pk,
                                'photo': ''},
                               HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 403)


class TestCreateTeamStatTestCase(TestCase):
    def setUp(self):
        self.team = TeamFactory()
        self.league = LeagueFactory()
        self.user_password = '1234'
        self.user = UserFactory(password=self.user_password)
        self.client = Client()
        self.client.login(username=self.user.username,
                          password=self.user_password)

    def test_create_with_valid_data(self):
        response = self.client.post('/fifa/api/teamstat/',
                                    {'team': self.team.pk,
                                     'league': self.league.pk},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'),
                         '"Team {} now in {}!"'.format(self.team.name,
                                                       self.league.name))

    def test_create_with_empty_fields(self):
        response = self.client.post('/fifa/api/teamstat/',
                                    {'team': '',
                                     'league': ''},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'),
                         'Please enter correct data!')

    def test_unauthenticated_user(self):
        client = Client()
        response = client.post('/fifa/api/teamstat/',
                               {'team': self.team.pk,
                                'league': self.league.pk},
                               HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 403)

    def test_authenticated_user_without_permissions(self):
        client = Client()
        User.objects.create_user(username='testuser', password='12345678')
        client.login(username='testuser', password='12345678')
        response = client.post('/fifa/api/teamstat/',
                               {'team': self.team.pk,
                                'league': self.league.pk},
                               HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 403)


class TestCreateMatchTestCase(TestCase):

    def setUp(self):
        self.league = LeagueFactory()
        self.team_home = TeamStatFactory(league=self.league)
        self.team_guest = TeamStatFactory(league=self.league)
        self.user_password = '1234'
        self.user = UserFactory(password=self.user_password)
        self.client = Client()
        self.client.login(username=self.user.username,
                          password=self.user_password)

    def test_create_with_valid_data(self):
        response = self.client.post('/fifa/api/match/',
                                    {'league': self.league.pk,
                                     'team_home': self.team_home.team.pk,
                                     'team_guest': self.team_guest
                                     .team.pk,
                                     'team_home_goals': 2,
                                     'team_guest_goals': 1},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'),
                         '"Match between {} and {} is created!"'
                         .format(self.team_home.team.name,
                                 self.team_guest.team.name))

    def test_unauthenticated_user(self):
        client = Client()
        response = client.post('/fifa/api/match/',
                               {'league': self.league.pk,
                                'team_home': self.team_home.team.pk,
                                'team_guest': self.team_guest
                                .team.pk,
                                'team_home_goals': 2,
                                'team_guest_goals': 1},
                               HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 403)

    def test_authenticated_user_without_permissions(self):
        client = Client()
        User.objects.create_user(username='testuser', password='12345678')
        client.login(username='testuser', password='12345678')
        response = client.post('/fifa/api/match/',
                               {'league': self.league.pk,
                                'team_home': self.team_home.team.pk,
                                'team_guest': self.team_guest
                                .team.pk,
                                'team_home_goals': 2,
                                'team_guest_goals': 1},
                               HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 403)


class TestCreateUserViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_with_valid_data(self):
        response = self.client.post('/fifa/create_user/',
                                    {'username': 'testuser',
                                     'password': '12345678',
                                     'password1': '12345678',
                                     'email': 'testuser@mail.com'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        user = User.objects.get(username='testuser')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(response.status_code, 200)
        self.assertIn('_auth_user_id', self.client.session)
        self.assertEqual('1', self.client.session['_auth_user_id'])

    def test_create_two_equal_user(self):
        self.client.post('/fifa/create_user/',
                         {'username': 'testuser',
                          'password': '12345678',
                          'email': 'testuser@mail.com'},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response = self.client.post('/fifa/create_user/',
                                    {'username': 'testuser',
                                     'password': '12345678',
                                     'email': 'testuser@mail.com'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'),
                         'Please enter correct data!')

    def test_create_two_users_with_equal_username(self):
        self.client.post('/fifa/create_user/',
                         {'username': 'testuser',
                          'password': '1234',
                          'email': 'testuser@mail.com'},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response = self.client.post('/fifa/create_user/',
                                    {'username': 'testuser',
                                     'password': '5678',
                                     'email': 'testuser@mail.com'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'),
                         'Please enter correct data!')

    def test_create_two_users_with_equal_passwords(self):
        self.client.post('/fifa/create_user/',
                         {'username': 'testuser1',
                          'password': '12345678',
                          'password1': '12345678',
                          'email': 'testuser1@mail.com'},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response = self.client.post('/fifa/create_user/',
                                    {'username': 'testuser2',
                                     'password': '12345678',
                                     'password1': '12345678',
                                     'email': 'testuser2@mail.com'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual('2', self.client.session['_auth_user_id'])

    def test_create_user_with_empty_data(self):
        response = self.client.post('/fifa/create_user/',
                                    {'username': '',
                                     'password': '',
                                     'email': 'testuser@mail.com'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'),
                         'Please enter correct data!')

    def test_create_user_with_empty_password(self):
        response = self.client.post('/fifa/create_user/',
                                    {'username': 'testuser',
                                     'password': '',
                                     'email': 'testuser@mail.com'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'),
                         'Please enter correct data!')

    def test_create_user_with_bad_confirm_password(self):
        response = self.client.post('/fifa/create_user/',
                                    {'username': 'testuser2',
                                     'password': '12345678',
                                     'password1': '1234',
                                     'email': 'testuser@mail.com'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'),
                         'Passwords not same!')

    def test_create_users_with_equal_emails(self):
        self.client.post('/fifa/create_user/',
                         {'username': 'testuser1',
                          'password': '12345678',
                          'password1': '12345678',
                          'email': 'testuser@mail.com'},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response = self.client.post('/fifa/create_user/',
                                    {'username': 'testuser2',
                                     'password': '12345678',
                                     'password1': '12345678',
                                     'email': 'testuser@mail.com'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'),
                         'This email already exists!')


class TestLoginUserViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.password = '12345678'
        self.user = UserFactory(username='testuser', password=self.password)

    def test_login_with_valid_data(self):
        response = self.client.post('/fifa/login_user/',
                                    {'username': 'testuser',
                                     'password': self.password},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertIn('_auth_user_id', self.client.session)
        self.assertEqual('1', self.client.session['_auth_user_id'])

    def test_login_with_empty_data(self):
        response = self.client.post('/fifa/login_user/',
                                    {'username': '',
                                     'password': ''},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'),
                         'Please enter correct data!')

    def test_login_with_bad_username(self):
        response = self.client.post('/fifa/login_user/',
                                    {'username': 'badtestuser',
                                     'password': self.password},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'),
                         'Bad login or password '
                         'or your account is disable!')

    def test_login_with_bad_password(self):
        response = self.client.post('/fifa/login_user/',
                                    {'username': 'testuser',
                                     'password': 'badpassword'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'),
                         'Bad login or password '
                         'or your account is disable!')

    def test_user_is_not_active(self):
        self.user.is_active = False
        self.user.save()
        response = self.client.post('/fifa/login_user/',
                                    {'username': 'testuser',
                                     'password': self.password},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'),
                         'Bad login or password '
                         'or your account is disable!')


class TestLogOutUserViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.password = '12345678'
        self.user = UserFactory(username='tetsuser', password=self.password)

    def test_logout_authenticated_user(self):
        self.client.login(username='testuser', password=self.password)
        response = self.client.get('/fifa/logout_user/')
        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertRedirects(response, '/fifa/')

    def test_logout_unauthenticated_user(self):
        response = self.client.get('/fifa/logout_user/')
        self.assertRedirects(response, '/fifa/')


class TestUserViewSetAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.password = '12345678'
        self.user = UserFactory(username='testuser', password=self.password)

    def test_change_password_with_get_method(self):
        self.client.login(username='testuser', password=self.password)
        response = self.client.get('/fifa/api/user/{}/change_password/')
        self.assertEqual(response.status_code, 405)

    def test_change_email_with_get_method(self):
        self.client.login(username='testuser', password=self.password)
        response = self.client.get('/fifa/api/user/{}/change_email/')
        self.assertEqual(response.status_code, 405)

    def test_change_password_with_valid_data(self):
        self.client.login(username='testuser', password=self.password)
        response = self.client.post('/fifa/api/user/{}/change_password/'
                                    .format(self.user.pk),
                                    {'old_password': self.password,
                                     'new_password1': '1234',
                                     'new_password2': '1234'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'),
                         'Password has changed!')

    def test_change_email_with_valid_data(self):
        self.client.login(username='testuser', password=self.password)
        response = self.client.post('/fifa/api/user/{}/change_email/'
                                    .format(self.user.pk),
                                    {'new_email': 'testuser1@mail.com'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'),
                         'Email has changed!')
        self.user = User.objects.get(username='testuser')
        self.assertEqual(self.user.email, 'testuser1@mail.com')

    def test_change_password_unauthenticated_user(self):
        response = self.client.post('/fifa/api/user/{}/change_password/'
                                    .format(self.user.pk),
                                    {'old_password': self.password,
                                     'new_password1': '1234',
                                     'new_password2': '1234'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 403)

    def test_change_email_unauthenticated_user(self):
        response = self.client.post('/fifa/api/user/{}/change_email/'
                                    .format(self.user.pk),
                                    {'old_password': self.password,
                                     'new_password1': '1234',
                                     'new_password2': '1234'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 403)

    def test_change_password_invalid_pk(self):
        self.client.login(username='testuser', password=self.password)
        response = self.client.post('/fifa/api/user/2/change_password/',
                                    {'old_password': self.password,
                                     'new_password1': '1234',
                                     'new_password2': '1234'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 403)

    def test_change_email_invalid_pk(self):
        self.client.login(username='testuser', password=self.password)
        response = self.client.post('/fifa/api/user/2/change_email/',
                                    {'new_email': 'testuser1@mail.com'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 403)

    def test_change_password_with_empty_data(self):
        self.client.login(username='testuser', password=self.password)
        response = self.client.post('/fifa/api/user/{}/change_password/'
                                    .format(self.user.pk),
                                    {'old_password': '',
                                     'new_password1': '',
                                     'new_password2': ''},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'),
                         'Please enter correct data!')

    def test_change_email_with_empty_data(self):
        self.client.login(username='testuser', password=self.password)
        response = self.client.post('/fifa/api/user/{}/change_email/'
                                    .format(self.user.pk),
                                    {'new_email': ''},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'),
                         'Please enter correct data!')

    def test_change_password_with_bad_old_password(self):
        self.client.login(username='testuser', password=self.password)
        response = self.client.post('/fifa/api/user/{}/change_password/'
                                    .format(self.user.pk),
                                    {'old_password': '5678',
                                     'new_password1': '1234',
                                     'new_password2': '1234'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'),
                         'Bad old password!')

    def test_change_email_with_the_same_email(self):
        self.client.login(username='testuser', password=self.password)
        response = self.client.post('/fifa/api/user/{}/change_email/'
                                    .format(self.user.pk),
                                    {'new_email': 'test_user@mail.com'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'),
                         'You cannot set the same emails!')

    def test_change_password_with_the_same_password(self):
        self.client.login(username='testuser', password=self.password)
        response = self.client.post('/fifa/api/user/{}/change_password/'
                                    .format(self.user.pk),
                                    {'old_password': '12345678',
                                     'new_password1': '12345678',
                                     'new_password2': '12345678'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'),
                         'You cannot set the same password!')

    def test_change_password_with_invalid_double_check_passwords(self):
        self.client.login(username='testuser', password=self.password)
        response = self.client.post('/fifa/api/user/{}/change_password/'
                                    .format(self.user.pk),
                                    {'old_password': self.password,
                                     'new_password1': '1234',
                                     'new_password2': '5678'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'),
                         'Please enter new passwords correctly!')
