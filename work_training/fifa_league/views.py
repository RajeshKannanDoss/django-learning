from django.views import View
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.db import DatabaseError
from django.utils.translation import ugettext as _
from django.contrib.auth import authenticate, login, logout

from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.decorators import list_route
from .serializers import LeagueSerializer, TeamSerializer

from .models import Team, TeamStat, League, Player
from .forms import UserCreateForm, LeagueCreateForm, TeamCreateForm, \
    PlayerCreateForm, TeamStatCreateForm, MatchCreateForm
from .functions import add_permissions_to_user, DEFAULT_PERMISSIONS


class UserFormsMixin:
    """
    Mixin for forms variables in template
    """
    def get_context_data(self, **kwargs):
        """
        :param kwargs:
        :return: forms for template
        """
        ctx = super().get_context_data(**kwargs)
        ctx.update(
            {
             'user_create_form': UserCreateForm(),
             'league_create_form': LeagueCreateForm(),
             'team_create_form': TeamCreateForm(),
             'player_create_form': PlayerCreateForm(),
             'teamstat_create_form': TeamStatCreateForm(),
             'match_create_form': MatchCreateForm()
            }
        )
        return ctx


class IndexView(UserFormsMixin, TemplateView):
    """
    Render list of all leagues and generate form fo user registration/login
    """
    template_name = 'leagues/leagues_list_view.html'

    def get_context_data(self, **kwargs):
        """
        :param kwargs:
        :return: list of all leagues
        """
        ctx = super().get_context_data(**kwargs)
        ctx.update({'leagues_list': League.objects.all()})
        return ctx


class TeamsListView(UserFormsMixin, TemplateView):
    """
    Render table of teams with statistic for specific League
    league_id - shortcut for League
    """
    template_name = 'leagues/teams_list_view.html'

    def get_context_data(self, **kwargs):
        """
        :return: list of TeamStat models object, order by points (best on top)
        """
        league_id = str(self.kwargs['league_shortcut'])

        league = get_object_or_404(League, shortcut=league_id)

        teams = league.teams_stat.order_by('points').reverse()

        ctx = super().get_context_data(**kwargs)
        ctx.update({'teams': teams})
        return ctx


class TeamView(UserFormsMixin, TemplateView):
    """
    Render Team statistic for specific League
    """
    template_name = 'teams/team_view.html'

    def get_context_data(self, **kwargs):
        """
        get league_shortcut and team_shortcut from URL,
        get specific team_stat then return
        :return: single TeamStat model object for template
        """
        league_id = str(self.kwargs['league_shortcut'])
        team_id = str(self.kwargs['team_shortcut'])

        league = get_object_or_404(League, shortcut=league_id)
        team = get_object_or_404(Team, shortcut=team_id)
        team_stat = get_object_or_404(team.leagues_stat,
                                      team=team,
                                      league=league)
        ctx = super().get_context_data(**kwargs)
        ctx.update({'team_stat': team_stat})
        return ctx


class CreateLeagueView(View):
    """
    Handle AJAX request and create new league
    """
    form_class = LeagueCreateForm

    def post(self, request):

        if not request.user.is_authenticated:
            return HttpResponse('Unauthorized request!', status=401)

        if not request.user.has_perm('fifa_league.add_league'):
            return HttpResponse('Forbidden!', status=403)

        form = self.form_class(request.POST)

        if not form.is_valid():
            return HttpResponse('Please enter correct data!', status=400)

        try:
            league = form.save(commit=False)
        except ValueError as e:
            return HttpResponse(e.args[0], status=400)

        league.name = form.cleaned_data['name']
        league.shortcut = form.cleaned_data['shortcut']

        if League.objects.filter(name=league.name).exists() or \
                League.objects.filter(shortcut=league.shortcut).exists():
            return HttpResponse(_('League {} already exist!')
                                .format(league.name), status=400)
        # TODO: Ask if this exception is good
        try:
            league.save()
        except DatabaseError as e:
            return HttpResponse(_('Database error! {}')
                                .format(e.args[0]), status=500)

        return HttpResponse(_('League {} is create!')
                            .format(league.name), status=200)


class CreateMatchView(View):
    """
    Handle AJAX request create new match and add points to related teams
    """
    form_class = MatchCreateForm

    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponse('Unauthorized request!', status=401)

        if not request.user.has_perm('fifa_league.add_match'):
            return HttpResponse('Forbidden!', status=403)

        form = self.form_class(request.POST)

        if not form.is_valid():
            return HttpResponse('Please enter correct data!', status=400)

        try:
            match = form.create()
        except ValueError as e:
            return HttpResponse(e.args[0], status=400)
        except DatabaseError as e:
            return HttpResponse(_('Database error! {}')
                                .format(e.args[0]), status=500)

        return HttpResponse(_('Match between {} and {} is created!')
                            .format(match.team_home.team.name,
                                    match.team_guest.team.name), status=200)


class CreateTeamView(View):
    """
    Handle AJAX request and create new team
    """
    form_class = TeamCreateForm

    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponse('Unauthorized request!', status=401)

        if not request.user.has_perm('fifa_league.add_team'):
            return HttpResponse('Forbidden!', status=403)

        form = self.form_class(request.POST)

        if not form.is_valid():
            return HttpResponse('Please enter correct data!', status=400)

        try:
            team = form.save(commit=False)
        except ValueError as e:
            return HttpResponse(e.args[0], status=400)

        # clean data
        team.name = form.cleaned_data['name']
        team.shortcut = form.cleaned_data['shortcut']

        # check if the same objects exists
        if Team.objects.filter(name=team.name).exists() or \
                Team.objects.filter(shortcut=team.shortcut).exists():
            return HttpResponse(_('Team {} already exist!')
                                .format(team.name), status=400)
        try:
            team.save()
        except DatabaseError as e:
            return HttpResponse(_('Database error! {}')
                                .format(e.args[0]), status=500)

        return HttpResponse(_('Team {} is created!')
                            .format(team.name), status=200)


class CreatePlayerView(View):
    """
    Handle AJAX request and create new player for specific team
    """
    form_class = PlayerCreateForm

    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponse('Unauthorized request!', status=401)

        if not request.user.has_perm('fifa_league.add_player'):
            return HttpResponse('Forbidden!', status=403)

        form = self.form_class(request.POST)
        if not form.is_valid():
            return HttpResponse('Please enter correct data!', status=400)

        try:
            player = form.save(commit=False)
        except ValueError as e:
            return HttpResponse(e.args[0], status=400)

        # clean data
        player.name = form.cleaned_data['name']
        player.age = form.cleaned_data['age']
        player.team = form.cleaned_data['team']

        # check if the same objects exists
        if Player.objects.filter(name=player.name).exists():
            return HttpResponse(_('Player {} already exist in {}!')
                                .format(player.name, player.team.name),
                                status=400)
        try:
            player.save()
        except DatabaseError as e:
            return HttpResponse(_('Database error! {}')
                                .format(e.args[0]), status=500)

        return HttpResponse(_('Player {} is created!')
                            .format(player.name), status=200)


class CreateTeamStatView(View):
    """
    Handle AJAX request and add specific team to league
    """
    form_class = TeamStatCreateForm

    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponse('Unauthorized request!', status=401)

        if not request.user.has_perm('fifa_league.add_teamstat'):
            return HttpResponse('Forbidden!', status=403)

        form = self.form_class(request.POST)

        if not form.is_valid():
            return HttpResponse('Please enter correct data!', status=400)

        try:
            teamstat = form.save(commit=False)
        except ValueError as e:
            return HttpResponse(e.args[0], status=400)

        teamstat.team = form.cleaned_data['team']
        teamstat.league = form.cleaned_data['league']

        if TeamStat.objects.filter(team=teamstat.team,
                                   league=teamstat.league).exists():
            return HttpResponse(_('Team already play in this league!'))

        try:
            teamstat.save()
        except DatabaseError as e:
            return HttpResponse(_('Database error! {}')
                                .format(e.args[0]), status=500)

        return HttpResponse(_('Team {} now in {}!')
                            .format(teamstat.team.name,
                                    teamstat.league.name), status=200)


class CreateUserView(View):
    """
    View for new user registration and than log in new user
    """
    form_class = UserCreateForm

    def post(self, request):
        """
        Handle POST request for user registration with UserCreateForm
        :param request:
        :return:
        """
        form = self.form_class(request.POST)

        if not form.is_valid():
            return HttpResponse('Please enter correct data!', status=400)

        try:
            user = form.save(commit=False)
        except ValueError as e:
            return HttpResponse(e.args[0], status=400)

        # clean (normalize) data
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']

        # set user credential and information
        user.username = username
        user.email = email
        user.set_password(password)
        user.save()

        # add default permission to user
        add_permissions_to_user(user, DEFAULT_PERMISSIONS)

        # login user
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('fifa_league:index')

        return HttpResponse("User didn't exist after saving!", status=500)


class LoginUserView(View):
    """
    View for user log in
    """

    def post(self, request):
        if request.is_ajax:
            username = str(request.POST.get('username', ''))
            password = str(request.POST.get('password', ''))
            if not username or not password:
                return HttpResponse(_('Some of the fields are empty!'),
                                    status=400)

            # log in user
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('fifa_league:index')
            else:
                return HttpResponse('Bad login or password!', status=400)
        else:
            return HttpResponse('Not AJAX!', status=400)


class LogOutUserView(View):
    """
    View for logout user and redirect to main page
    """

    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return redirect('fifa_league:index')


class LeagueList(generics.ListCreateAPIView):
    """
    REST API View | generates list of all Leagues and send
    """
    queryset = League.objects.all()
    serializer_class = LeagueSerializer


class TeamViewSet(viewsets.ViewSet):
    """
    Simple viewset for Team API
    """

    def list(self, request):
        """
        :param request:
        :return: List of all teams
        """
        queryset = Team.objects.all()
        serializer = TeamSerializer(queryset, many=True)
        return Response(serializer.data)

    @list_route(methods=['get'],
                url_path='get_teams_from_league/'
                         '(?P<league_shortcut>[0-9a-zA-Z]+)')
    def get_teams_from_league(self, request, *args, **kwargs):
        """
        :param kwargs: contains league_shortcut
        :return: list of team related to league
        """
        shortcut = self.kwargs.get('league_shortcut')
        queryset = Team.objects.filter(leagues_stat__in=TeamStat.objects
                                       .filter(league__shortcut=shortcut))
        serializer = TeamSerializer(queryset, many=True)
        return Response(serializer.data)
