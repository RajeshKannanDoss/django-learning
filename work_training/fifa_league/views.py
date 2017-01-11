from django.views import View
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseForbidden, \
    HttpResponseBadRequest, HttpResponseServerError, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.db import DatabaseError
from django.utils.translation import ugettext as _
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.decorators import list_route, detail_route
from .serializers import LeagueSerializer, TeamSerializer

from .models import Team, TeamStat, League, Player
from .forms import UserCreateForm, LeagueCreateForm, TeamCreateForm, \
    PlayerCreateForm, TeamStatCreateForm, MatchCreateForm, UserLoginForm, \
    UserChangePasswordForm, UserChangeEmailForm, UserAvatarUploadForm
from .functions import add_permissions_to_user, DEFAULT_PERMISSIONS

from .mixins import UserFormsMixin, UserPermissionsCheckMixin, AjaxCheckMixin,\
    UserAuthenticationCheckMixin


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


class UserSettingsView(UserAuthenticationCheckMixin,
                       UserFormsMixin, TemplateView):
    """
    Render template to change user settings
    """
    template_name = 'user/settings.html'

    def get_context_data(self, **kwargs):
        """
        Update get_context data and add new forms for user settings
        :param kwargs:
        :return:
        """
        ctx = super().get_context_data(**kwargs)
        ctx.update({'user_change_password_form': UserChangePasswordForm(),
                    'user_change_email_form': UserChangeEmailForm()})
        return ctx


class CreateLeagueView(AjaxCheckMixin, UserAuthenticationCheckMixin,
                       UserPermissionsCheckMixin, View):
    """
    Handle AJAX request and create new league
    """
    form_class = LeagueCreateForm
    permissions_required = ['add_league']

    def post(self, request):
        form = self.form_class(request.POST)

        if not form.is_valid():
            return HttpResponseBadRequest('Please enter correct data!')

        try:
            league = form.save(commit=False)
        except ValueError as e:
            return HttpResponseBadRequest(e.args[0])

        league.name = form.cleaned_data['name']
        league.shortcut = form.cleaned_data['shortcut']

        if League.objects.filter(name=league.name).exists() or \
                League.objects.filter(shortcut=league.shortcut).exists():
            return HttpResponseBadRequest(_('League {} already exist!')
                                          .format(league.name))

        league.save()

        return HttpResponse(_('League {} is create!')
                            .format(league.name))


class CreateMatchView(AjaxCheckMixin, UserAuthenticationCheckMixin,
                      UserPermissionsCheckMixin, View):
    """
    Handle AJAX request create new match and add points to related teams
    """
    form_class = MatchCreateForm
    permissions_required = ['add_match']

    def post(self, request):
        form = self.form_class(request.POST)

        if not form.is_valid():
            return HttpResponseBadRequest('Please enter correct data!')

        try:
            match = form.create()
        except ValueError as e:
            return HttpResponseBadRequest(e.args[0])
        except DatabaseError as e:
            return HttpResponseServerError(_('Database error! {}')
                                           .format(e.args[0]))

        return HttpResponse(_('Match between {} and {} is created!')
                            .format(match.team_home.team.name,
                                    match.team_guest.team.name))


class CreateTeamView(AjaxCheckMixin, UserAuthenticationCheckMixin,
                     UserPermissionsCheckMixin, View):
    """
    Handle AJAX request and create new team
    """
    form_class = TeamCreateForm
    permissions_required = ['add_team']

    def post(self, request):
        form = self.form_class(request.POST)

        if not form.is_valid():
            return HttpResponseBadRequest('Please enter correct data!')

        try:
            team = form.save(commit=False)
        except ValueError as e:
            return HttpResponseBadRequest(e.args[0])

        team.name = form.cleaned_data['name']
        team.shortcut = form.cleaned_data['shortcut']

        if Team.objects.filter(name=team.name).exists() or \
                Team.objects.filter(shortcut=team.shortcut).exists():
            return HttpResponseBadRequest(_('Team {} already exist!')
                                          .format(team.name))

        team.save()

        return HttpResponse(_('Team {} is created!')
                            .format(team.name))


class CreatePlayerView(AjaxCheckMixin, UserAuthenticationCheckMixin,
                       UserPermissionsCheckMixin, View):
    """
    Handle AJAX request and create new player for specific team
    """
    form_class = PlayerCreateForm
    permissions_required = ['add_player']

    def post(self, request):
        form = self.form_class(request.POST)

        if not form.is_valid():
            return HttpResponseBadRequest('Please enter correct data!')

        try:
            player = form.save(commit=False)
        except ValueError as e:
            return HttpResponseBadRequest(e.args[0])

        player.name = form.cleaned_data['name']
        player.age = form.cleaned_data['age']
        player.team = form.cleaned_data['team']

        if Player.objects.filter(name=player.name).exists():
            return HttpResponseBadRequest(_('Player {} already exist in {}!')
                                          .format(player.name,
                                                  player.team.name))

        player.save()

        return HttpResponse(_('Player {} is created!')
                            .format(player.name))


class CreateTeamStatView(AjaxCheckMixin, UserAuthenticationCheckMixin,
                         UserPermissionsCheckMixin, View):
    """
    Handle AJAX request and add specific team to league
    """
    form_class = TeamStatCreateForm
    permissions_required = ['add_teamstat']

    def post(self, request):
        form = self.form_class(request.POST)

        if not form.is_valid():
            return HttpResponseBadRequest('Please enter correct data!')

        try:
            teamstat = form.save(commit=False)
        except ValueError as e:
            return HttpResponseBadRequest(e.args[0])

        teamstat.team = form.cleaned_data['team']
        teamstat.league = form.cleaned_data['league']

        if TeamStat.objects.filter(team=teamstat.team,
                                   league=teamstat.league).exists():
            return HttpResponseBadRequest(
                _('Team already play in this league!'))

        teamstat.save()

        return HttpResponse(_('Team {} now in {}!')
                            .format(teamstat.team.name,
                                    teamstat.league.name))


class CreateUserView(AjaxCheckMixin, View):
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
            return HttpResponseBadRequest('Please enter correct data!')

        try:
            user = form.save(commit=False)
        except ValueError as e:
            return HttpResponseBadRequest(e.args[0])

        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        password1 = form.cleaned_data['password1']
        email = form.cleaned_data['email']

        if not password == password1:
            return HttpResponseBadRequest('Passwords not same!')

        if User.objects.filter(email=email).exists():
            return HttpResponseBadRequest('This email already exists!')

        user.username = username
        user.email = email
        user.set_password(password)
        user.save()

        # add default permission to user
        add_permissions_to_user(user, DEFAULT_PERMISSIONS)

        user = authenticate(username=username, password=password)

        if user is None:
            return HttpResponseServerError("User didn't exist after saving!")

        if not user.is_active:
            return HttpResponseForbidden('Your account is disabled!')

        login(request, user)
        return HttpResponse('User {} is created! Welcome!'
                            .format(user.username))


class LoginUserView(AjaxCheckMixin, View):
    """
    View for user log in
    """
    form_class = UserLoginForm

    def post(self, request):
        form = UserLoginForm(request.POST)

        if not form.is_valid():
            return HttpResponseBadRequest('Please enter correct data!')

        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(username=username, password=password)

        if user is None:
            return HttpResponseBadRequest('Bad login or password!')

        if not user.is_active:
            return HttpResponseForbidden('Your account is disabled!')

        login(request, user)
        return HttpResponse('Welcome {}!'
                            .format(user.username))


class LogOutUserView(View):
    """
    View for logout user and redirect to main page
    """

    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return redirect('fifa_league:index')


class UserAvatarUploadView(View):
    """
    User view to handle avatar upload
    """
    def post(self, request):
        form = UserAvatarUploadForm(request.POST, request.FILES,
                                    instance=request.user.profile)
        if not form.is_valid():
            response = {'is_valid': False,
                        'message': 'Invalid data!'}
            return JsonResponse(response)

        profile = form.save()
        response = {'is_valid': True,
                    'url': profile.avatar.url,
                    'message': 'Your avatar successfully upload!'}
        return JsonResponse(response)


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


class UserViewSet(viewsets.ViewSet):
    """
    User viewsets for handle users action
    """

    @detail_route(['POST'])
    def change_password(self, request, pk, *args, **kwargs):
        """
        API for change user password
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        if not request.is_ajax():
            return HttpResponseBadRequest('AJAX is required!')

        if not request.user.is_authenticated:
            return HttpResponse(status=401)

        # Very important for security
        if not str(request.user.pk) == pk:
            return HttpResponseForbidden('No no no!')

        form = UserChangePasswordForm(request.POST)

        if not form.is_valid():
            return HttpResponseBadRequest('Please enter correct data!')

        old_password = form.cleaned_data['old_password']
        new_password1 = form.cleaned_data['new_password1']
        new_password2 = form.cleaned_data['new_password2']

        user = authenticate(username=request.user.username,
                            password=old_password)
        if user is None:
            return HttpResponseBadRequest('Bad old password!')

        if not new_password1 == new_password2:
            return HttpResponseBadRequest(
                'Please enter new passwords correctly!')

        if new_password1 == old_password:
            return HttpResponseBadRequest('You cannot set the same password!')

        user.set_password(new_password1)
        user.save()
        login(request, user)
        return HttpResponse('Password has changed!')

    @detail_route(['POST'])
    def change_email(self, request, pk, *args, **kwargs):
        """
        API for change user email
        :return:
        """
        if not request.is_ajax():
            return HttpResponseBadRequest('AJAX is required!')

        if not request.user.is_authenticated:
            return HttpResponse(status=401)

        # Very important for security
        if not str(request.user.pk) == pk:
            return HttpResponseForbidden('No no no!')

        form = UserChangeEmailForm(request.POST)

        if not form.is_valid():
            return HttpResponseBadRequest('Please enter correct data!')

        new_email = form.cleaned_data['new_email']

        if new_email == request.user.email:
            return HttpResponseBadRequest('You cannot set the same emails!')

        request.user.email = new_email
        request.user.save()
        return HttpResponse('Email has changed!')
