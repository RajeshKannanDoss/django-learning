from django.views import View
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseForbidden, \
    HttpResponseBadRequest, HttpResponseServerError, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.db import DatabaseError
from django.db.models import Q
from django.utils.translation import ugettext as _
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import list_route, detail_route
from rest_framework.permissions import IsAuthenticatedOrReadOnly, \
    IsAuthenticated
from .serializers import LeagueSerializer, TeamSerializer, \
    TeamStatSerializer, MatchSerializer, PlayerSerializer

from .models import Team, TeamStat, League, Player, Match
from .forms import UserCreateForm, LeagueCreateForm, TeamCreateForm, \
    PlayerCreateForm, TeamStatCreateForm, MatchCreateForm, UserLoginForm, \
    UserChangePasswordForm, UserChangeEmailForm, UserAvatarUploadForm
from .functions import add_permissions_to_user, DEFAULT_PERMISSIONS

from .mixins import UserFormsMixin


class IndexView(UserFormsMixin, TemplateView):
    """
    Render list of all leagues and generate form fo user registration/login
    """
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        """
        :param kwargs:
        :return: list of all leagues
        """
        ctx = super().get_context_data(**kwargs)
        ctx.update({'leagues_list': League.objects.all()})
        return ctx


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

        login(request, user)
        return HttpResponse('User {} is created! Welcome!'
                            .format(user.username))


class LoginUserView(View):
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
            return HttpResponseBadRequest('Bad login or password '
                                          'or your account is disable!')

        login(request, user)
        return HttpResponse('Welcome {}!'
                            .format(user.username))


class LogOutUserView(View):
    """
    View for logout user and redirect to main page
    """

    def get(self, request):
        logout(request)
        return redirect('fifa_league:index')


class LeagueViewSet(viewsets.ModelViewSet):
    """
    REST API View | generates list of all Leagues and send
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request):
        queryset = League.objects.all()
        serializer = LeagueSerializer(queryset, many=True)
        return Response(serializer.data)

    @list_route(['GET'], url_path='(?P<pk>[0-9]+)/get_teams')
    def get_teams(self, request, *args, **kwargs):
        """
        :param kwargs: contains league_shortcut
        :return: list of team related to league
        """
        pk = self.kwargs['pk']
        queryset = Team.objects.filter(leagues_stat__in=TeamStat.objects
                                       .filter(league__pk=pk))
        serializer = TeamSerializer(queryset, many=True)
        return Response(serializer.data)

    @detail_route(['DELETE'])
    def delete(self, request, pk, *args, **kwargs):
        league = get_object_or_404(League, pk=pk)

        if league.author != request.user:
            return HttpResponseForbidden('No no no!')

        league.delete()
        return Response(status=204)

    def retrieve(self, request, pk, *args, **kwargs):
        # only auth user can get info about particular league
        if not request.user.is_authenticated:
            return HttpResponse(status=401)

        league = get_object_or_404(League, pk=pk)

        if league.author != request.user:
            return HttpResponseForbidden('No no no!')

        serializer = LeagueSerializer(league)
        return Response(serializer.data)

    @detail_route(['GET'])
    def get_teamstat_list(self, request, pk, *args, **kwargs):
        teamstats = TeamStat.objects.filter(league__pk=pk)\
            .order_by('points').reverse()

        serializer = TeamStatSerializer(teamstats, many=True)
        return Response(serializer.data)

    def update(self, request, pk, *args, **kwargs):
        league = get_object_or_404(League, pk=pk)

        if league.author != request.user:
            return HttpResponseForbidden('No no no')

        form = LeagueCreateForm(request.POST, request.FILES, instance=league)
        if not form.is_valid():
            return Response(form.errors, status=422)

        form.save()
        return Response('Object is updated!')

    def create(self, request):
        if not request.user.has_perm('fifa_league.add_league'):
            return HttpResponseForbidden()

        form = LeagueCreateForm(request.POST, request.FILES)

        if not form.is_valid():
            return HttpResponseBadRequest('Please enter correct data!')

        try:
            league = form.save(commit=False)
        except ValueError as e:
            return HttpResponseBadRequest(e.args[0])

        league.name = form.cleaned_data['name']
        league.short_description = form.cleaned_data['short_description']
        league.full_description = form.cleaned_data['full_description']
        league.author = request.user

        if League.objects.filter(name=league.name).exists():
            return HttpResponseBadRequest(_('League {} already exist!')
                                          .format(league.name))

        league.save()

        return Response(_('League {} is create!')
                        .format(league.name))


class TeamViewSet(viewsets.ViewSet):
    """
    Simple viewset for Team API
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request):
        """
        :param request:
        :return: List of all teams
        """
        queryset = Team.objects.all()
        serializer = TeamSerializer(queryset, many=True)
        return Response(serializer.data)

    @detail_route(['GET'])
    def get_players(self, request, pk, *args, **kwargs):
        players = Player.objects.filter(team__pk=pk)
        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data)

    def create(self, request):
        if not request.user.has_perm('fifa_league.add_team'):
            return HttpResponseForbidden()

        form = TeamCreateForm(request.POST, request.FILES)

        if not form.is_valid():
            return HttpResponseBadRequest('Please enter correct data!')

        try:
            team = form.save(commit=False)
        except ValueError as e:
            return HttpResponseBadRequest(e.args[0])

        team.name = form.cleaned_data['name']
        team.description = form.cleaned_data['description']
        team.author = request.user

        if Team.objects.filter(name=team.name).exists():
            return HttpResponseBadRequest(_('Team {} already exist!')
                                          .format(team.name))

        team.save()

        return Response(_('Team {} is created!')
                        .format(team.name))


class UserViewSet(viewsets.ViewSet):
    """
    User viewsets for handle users action
    """
    permission_classes = (IsAuthenticated, )

    @detail_route(['POST'])
    def change_password(self, request, pk, *args, **kwargs):
        """
        API for change user password
        :param request:
        :param args:
        :param kwargs:
        :param pk:
        :return:
        """
        # Very important for security
        if not str(request.user.pk) == pk:
            return HttpResponseForbidden('Invalid pk '
                                         'identificator for user and request')

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

    @detail_route(['POST'])
    def change_avatar(self, request, pk, *args, **kwargs):
        if not str(request.user.pk) == pk:
            return HttpResponseForbidden()

        old_filename = request.user.profile.avatar.name
        form = UserAvatarUploadForm(request.POST, request.FILES,
                                    instance=request.user.profile)
        if not form.is_valid():
            response = {'is_valid': False,
                        'message': 'Invalid data!'}
            return JsonResponse(response, status=400)

        if old_filename != '../media/static/fifa_league' \
                           '/user/default-avatar.svg':
            request.user.profile.avatar.storage.delete(old_filename)

        profile = form.save()
        response = {'is_valid': True,
                    'url': profile.avatar.url,
                    'message': 'Your avatar successfully upload!'}
        return JsonResponse(response)

    @list_route(['GET'])
    def get_user_leagues(self, request):
        leagues = League.objects.filter(author=request.user)
        serializer = LeagueSerializer(leagues, many=True)
        return Response(serializer.data)


class TeamStatViewSet(viewsets.ViewSet):
    """
    TeamStat viewset
    """
    permission_classes = (IsAuthenticatedOrReadOnly, )

    @detail_route(['GET'])
    def get_info(self, request, pk, *args, **kwargs):
        teamstat = get_object_or_404(TeamStat, pk=pk)

        serializer = TeamStatSerializer(teamstat)
        return Response(serializer.data)

    @detail_route(['GET'])
    def get_matches(self, request, pk, *args, **kwargs):
        matches = Match.objects.filter(Q(team_home=pk)
                                       | Q(team_guest=pk))
        serializer = MatchSerializer(matches, many=True)
        return Response(serializer.data)

    @detail_route(['GET'])
    def get_team(self, request, pk, *args, **kwargs):
        team = get_object_or_404(Team, leagues_stat__pk=pk)
        serializer = TeamSerializer(team)
        return Response(serializer.data)

    def create(self, request):
        if not request.user.has_perm('fifa_league.add_teamstat'):
            return HttpResponseForbidden()

        form = TeamStatCreateForm(request.POST)

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

        return Response(_('Team {} now in {}!')
                        .format(teamstat.team.name,
                                teamstat.league.name))


class MatchViewSet(viewsets.ViewSet):
    """
    Viewset for match and related objects
    """
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        if not request.user.has_perm('fifa_league.add_match'):
            return HttpResponseForbidden()

        form = MatchCreateForm(request.POST)

        if not form.is_valid():
            return HttpResponseBadRequest('Please enter correct data!')

        try:
            match = form.create()
        except ValueError as e:
            return HttpResponseBadRequest(e.args[0])
        except DatabaseError as e:
            return HttpResponseServerError(_('Database error! {}')
                                           .format(e.args[0]))

        return Response(_('Match between {} and {} is created!')
                        .format(match.team_home.team.name,
                                match.team_guest.team.name))


class PlayerViewSet(viewsets.ViewSet):
    """
    Viewset for Player model and related objects
    """
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        if not request.user.has_perm('fifa_league.add_player'):
            return HttpResponseForbidden()

        form = PlayerCreateForm(request.POST, request.FILES)

        if not form.is_valid():
            return HttpResponseBadRequest('Please enter correct data!')

        try:
            player = form.save(commit=False)
        except ValueError as e:
            return HttpResponseBadRequest(e.args[0])

        player.name = form.cleaned_data['name']
        player.age = form.cleaned_data['age']
        player.team = form.cleaned_data['team']
        player.author = request.user

        if Player.objects.filter(name=player.name).exists():
            return HttpResponseBadRequest(_('Player {} already exist!')
                                          .format(player.name))

        player.save()

        return Response(_('Player {} is created!')
                        .format(player.name))
