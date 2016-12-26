from django.views import View
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError
from django.db import DatabaseError
from django.utils.translation import ugettext as _

from rest_framework import generics
from .serializers import LeagueSerializer, TeamSerializer

from .models import Team, TeamStat, Match, League, Player
from .functions import post_save, add_points_to_teams


class IndexView(View):
    """
    Render all leagues view
    """
    def get(self, request):
        leagues_list = League.objects.all()
        return render(request, 'leagues/leagues_list_view.html',
                      {'leagues_list': leagues_list})


class TeamsListView(View):
    """
    Render teams list for specific league
    """
    def get(self, request, **kwargs):
        try:
            league_id = str(self.kwargs['league_id'])
        except KeyError as e:
            return HttpResponse('[!] Bad key! {}'.format(e.args[0]), status=400)

        league = get_object_or_404(League, shortcut=league_id)

        teams = league.teams_stat.order_by('points').reverse()

        return render(request, 'leagues/teams_list_view.html',
                      {'teams': teams, 'league': league})


class TeamView(View):
    """
    Render team view for specific league
    """
    def get(self, request, **kwargs):
        try:
            league_id = str(self.kwargs['league_id'])
            team_id = str(self.kwargs['team_id'])
        except KeyError as e:
            return HttpResponse('[!] Bad key! {}'.format(e.args[0]), status=400)

        league = get_object_or_404(League, shortcut=league_id)
        team = get_object_or_404(Team, shortcut=team_id)
        team_stat = get_object_or_404(team.leagues_stat, team=team, league=league)

        return render(request, 'teams/team_view.html',
                      {'team_stat': team_stat})


class CreateLeagueView(View):
    """
    Handle AJAX request and create new league
    """
    def post(self, request):
        try:
            league_name = str(request.POST.get('name', ''))
            league_shortcut = str(request.POST.get('shortcut', ''))
            if not league_name or not league_shortcut:
                return HttpResponse(_('[!] Some of the request variables is empty'), status=400)

        except MultiValueDictKeyError as e:
            return HttpResponse('[!] Value key error in {} while request!'.format(e.args[0]), status=400)

        if League.objects.filter(name=league_name).exists() or League.objects.filter(shortcut=league_shortcut).exists():
            return HttpResponse('League {} already exist!'.format(league_name))

        try:
            league = League.objects.create(name=league_name, shortcut=league_shortcut)
            league.save()
        except DatabaseError as e:
            return HttpResponse('[!] Database error! {}'.format(e.args[0]), status=500)

        return HttpResponse('League {} is create!'.format(league_name), status=200)


class CreateMatchView(View):
    """
    Handle AJAX request create new match and add points to related teams
    """
    def post(self, request):
        try:
            league_request = str(request.POST.get('league', ''))
            home_team_request = str(request.POST.get('home_team', ''))
            guest_team_request = str(request.POST.get('guest_team', ''))
            home_score = int(request.POST.get('home_score', 0))
            guest_score = int(request.POST.get('guest_score', 0))
            if not league_request or not home_team_request or not guest_team_request \
                    or not home_score or not guest_score:
                return HttpResponse(_('[!] Some of the request variables is empty'), status=400)

        except MultiValueDictKeyError as e:
            return HttpResponse('[!] Value key error in {} while request!'.format(e.args[0]), status=400)
        except ValueError as e:
            return HttpResponse(e.args[0] + _('[!] Please enter number!'), status=400)

        try:
            league = League.objects.get(shortcut=league_request)
            home_team = Team.objects.get(shortcut=home_team_request)
            guest_team = Team.objects.get(shortcut=guest_team_request)

            if home_team == guest_team:
                return HttpResponse(_('[!] Choose different teams!'))

            home_stat = TeamStat.objects.get(team=home_team, league=league)
            guest_stat = TeamStat.objects.get(team=guest_team, league=league)
        except League.DoesNotExist as e:
            return HttpResponse(e.args[0], status=500)
        except Team.DoesNotExist as e:
            return HttpResponse(e.args[0], status=500)
        except TeamStat.DoesNotExist as e:
            return HttpResponse(e.args[0], status=500)

        try:
            match = Match.objects.create(team_home=home_stat, team_guest=guest_stat, team_home_goals=home_score,
                                         team_guest_goals=guest_score)
            match.save()
        except DatabaseError as e:
            return HttpResponse('[!] Database error! {}'.format(e.args[0]), status=500)

        return HttpResponse('Match between {} and {} is created!'.format(home_team.name, guest_team.name), status=200)


class CreateTeamView(View):
    """
    Handle AJAX request and create new team
    """
    def post(self, request):
        try:
            team_name = str(request.POST.get('team_name', ''))
            team_shortcut = str(request.POST.get('team_shortcut', ''))
            if not team_name or not team_shortcut:
                return HttpResponse('[!] Some of the request variables is empty', status=400)

        except MultiValueDictKeyError as e:
            return HttpResponse('[!] Value key error in {} while request!'.format(e.args[0]), status=400)

        if Team.objects.filter(name=team_name).exists() or Team.objects.filter(shortcut=team_shortcut).exists():
            return HttpResponse('Team {} already exist!'.format(team_name), status=400)

        try:
            team = Team.objects.create(name=team_name, shortcut=team_shortcut)
            team.save()
        except DatabaseError as e:
            return HttpResponse('[!] Database error! {}'.format(e.args[0]), status=500)

        return HttpResponse('Team {} is created!'.format(team_name), status=200)


class CreatePlayerView(View):
    """
    Handle AJAX request and create new player for specific team
    """
    def post(self, request):
        try:
            player_name = str(request.POST.get('player_name', ''))
            player_age = int(request.POST.get('player_age', 0))
            player_team = str(request.POST.get('player_team', ''))
            if not player_name or not player_age or not player_team:
                return HttpResponse('[!] Some of the request variables is empty', status=400)

        except MultiValueDictKeyError as e:
            return HttpResponse('[!] Value key error in {} while request!'.format(e.args[0]), status=400)
        except ValueError as e:
            return HttpResponse(e.args[0] + _('[!] Please enter number!'), status=400)

        try:
            team = Team.objects.get(shortcut=player_team)
        except Team.DoesNotExist as e:
            return HttpResponse(e.args[0], status=500)

        if Player.objects.filter(team=team, name=player_name).exists():
            return HttpResponse('[!] Player {} already exist in {}!'.format(player_name, player_team), status=400)

        try:
            player = Player.objects.create(team=team, name=player_name, age=player_age)
            player.save()
        except DatabaseError as e:
            return HttpResponse('[!] Database error! {}'.format(e.args[0]), status=500)

        return HttpResponse('Player {} is created!'.format(player_name), status=200)


class AddTeamToLeagueView(View):
    """
    Handle AJAX request and add specific team to league
    """
    def post(self, request):
        try:
            team_name = str(request.POST.get('team_name', ''))
            league_name = str(request.POST.get('league_name', ''))
            if not team_name or not league_name:
                return HttpResponse('[!] Some of the request variables is empty', status=400)

        except MultiValueDictKeyError as e:
            return HttpResponse('[!] Value key error in {} while request!'.format(e.args[0]), status=400)

        try:
            team = Team.objects.get(shortcut=team_name)
            league = League.objects.get(shortcut=league_name)
        except League.DoesNotExist as e:
            return HttpResponse(e.args[0], status=500)
        except Team.DoesNotExist as e:
            return HttpResponse(e.args[0], status=500)

        if TeamStat.objects.filter(team=team, league=league).exists():
            return HttpResponse('Team already play in this league!')

        try:
            team_stat = TeamStat.objects.create(team=team, league=league)
            team_stat.save()
        except DatabaseError as e:
            return HttpResponse('[!] Database error! {}'.format(e.args[0]), status=500)

        return HttpResponse('Team {} now in {}!'.format(team_name, league_name), status=200)


class LeagueList(generics.ListCreateAPIView):
    """
    REST API View | generates list of all Leagues and send
    """
    queryset = League.objects.all()
    serializer_class = LeagueSerializer


class TeamListFromLeague(generics.ListAPIView):
    """
    REST API View | get league_shortcut from urls,
    then send all teams object related to specific League
    """
    serializer_class = TeamSerializer
    lookup_url_kwarg = 'league_shortcut'

    def get_queryset(self):
        """
        :return: if find League and all teams_stat - send list of all teams
        else send None
        """
        teams_list = []
        shortcut = self.kwargs.get(self.lookup_url_kwarg)

        try:
            teams_stat_list = League.objects.get(shortcut=shortcut).teams_stat.all()
        except League.DoesNotExist:
            return None

        for team_stat in teams_stat_list:
            teams_list.append(team_stat.team)

        return teams_list


class TeamList(generics.ListCreateAPIView):
    """
    REST API | generates list of all teams and send
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
