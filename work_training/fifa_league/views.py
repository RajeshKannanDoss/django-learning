# -*- coding: utf-8 -*-
from .models import *
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .functions import url_to_id, add_points_to_team
from django.utils.datastructures import MultiValueDictKeyError
from django.db import DatabaseError

from django.utils.translation import ugettext as _


class IndexView(View):
    """
    Render all leagues
    """
    def get(self, request):
        leagues_list = League.objects.all()
        teams = Team.objects.all()
        return render(request, 'leagues/leagues_list_view.html', {'leagues_list': leagues_list, 'teams': teams})


class TeamsListView(View):
    """
    Render teams list for specific league
    """
    def get(self, request, **kwargs):
        try:
            league_id = str(self.kwargs['league_id'])
        except KeyError as e:
            return HttpResponse("[!] Bad key!" + e.args[0], status=400)

        league = url_to_id(league_id, League)
        if league:
            teams = league.teams_stat.order_by("points").reverse()
            leagues_list = League.objects.all()
        else:
            return HttpResponse("Requested object doesn't exist!", status=500)
        return render(request, 'leagues/teams_list_view.html',
                      {'teams': teams, 'leagues_list': leagues_list, 'league': league})


class TeamView(View):
    """
    Render team view for specific league
    """
    def get(self, request, **kwargs):
        try:
            league_id = str(self.kwargs['league_id'])
            team_id = str(self.kwargs['team_id'])
        except KeyError as e:
            return HttpResponse("[!] Bad key!" + e.args[0], status=400)

        try:
            league = League.objects.get(shortcut=league_id)
            team = Team.objects.get(shortcut=team_id)
            team_stat = team.leagues_stat.get(team=team, league=league)
        except League.DoesNotExist:
            return HttpResponse("League requested object doesn't exist!", status=500)
        except Team.DoesNotExist:
            return HttpResponse("Team requested object doesn't exist!", status=500)
        except TeamStat.DoesNotExist:
            return HttpResponse("TeamStat requested object doesn't exist!", status=500)

        leagues_list = League.objects.all()
        return render(request, 'teams/team_view.html',
                      {'team': team, 'team_stat': team_stat, 'leagues_list': leagues_list})


class GetData(View):
    """
    Response AJAX requests from client
    """
    def post(self, request):
        if request.is_ajax:
            try:
                action = str(request.POST['action'])
                if not action:
                    return HttpResponse(_("[!] Error! action is empty!"), status=400)
            except MultiValueDictKeyError as e:
                return HttpResponse("[!] Value key error in " + e.args[0] + " while request!", status=400)

            response = []
            response_data = {}
            if action == 'get_teams_list_from_league':
                try:
                    league_shortcut = request.POST['league_shortcut']
                    if not league_shortcut:
                        return HttpResponse(_("[!] Error! league_shortcut is empty!"), status=400)
                except MultiValueDictKeyError as e:
                    return HttpResponse("[!] Value key error in " + e.args[0] + " while request!", status=400)

                try:
                    teams_stat_list = League.objects.get(shortcut=league_shortcut).teams_stat.all()
                except League.DoesNotExist as e:
                    return HttpResponse(e.args[0], status=500)

                for team_stat in teams_stat_list:
                    response.append(team_stat.team.name)
                response_data['teams_names'] = response

                return JsonResponse(response_data)
            elif action == 'get_teams_list':
                teams = Team.objects.all()
                for team in teams:
                    response.append(team.name)
                response_data['teams_names'] = response
                return JsonResponse(response_data)
            else:
                return HttpResponse("No requested action find on server!", status=400)
        else:
            return HttpResponse("AJAX request is required!", status=400)


class CreateLeague(View):
    """
    Handle AJAX request and create new league
    """
    def post(self, request):
        try:
            league_name = str(request.POST['name'])
            league_shortcut = str(request.POST['shortcut'])
            if not league_name or not league_shortcut:
                return HttpResponse(_("[!] Some of the request variables is empty"), status=400)
        except MultiValueDictKeyError as e:
            return HttpResponse("[!] Value key error in " + e.args[0] + " while request!", status=400)

        if League.objects.filter(name=league_name) or League.objects.filter(shortcut=league_shortcut):
            return HttpResponse("League " + league_name + " already exist!")

        try:
            league = League.objects.create(name=league_name, shortcut=league_shortcut)
            league.save()
        except DatabaseError as e:
            return HttpResponse("[!] Database error! " + e.args[0], status=500)
        return HttpResponse("League " + league_name + " is create!")


class CreateMatch(View):
    """
    Handle AJAX request create new match and add points to related teams
    """
    def post(self, request):
        try:
            league_request = str(request.POST['league'])
            home_team_request = str(request.POST['home_team'])
            guest_team_request = str(request.POST['guest_team'])
            home_score = int(request.POST['home_score'])
            guest_score = int(request.POST['guest_score'])
            if not league_request or not home_team_request or not guest_team_request \
                    or not home_score or not guest_score:
                return HttpResponse(_("[!] Some of the request variables is empty"), status=400)

        except MultiValueDictKeyError as e:
            return HttpResponse("[!] Value key error in " + e.args[0] + " while request!", status=400)
        except ValueError as e:
            return HttpResponse(e.args[0] + _("[!] Please enter number!"), status=400)

        try:
            league = League.objects.get(shortcut=league_request)
            home_team = Team.objects.get(name=home_team_request)
            guest_team = Team.objects.get(name=guest_team_request)

            if home_team == guest_team:
                return HttpResponse(_("[!] Choose different teams!"))

            home_stat = TeamStat.objects.get(team=home_team, league=league)
            guest_stat = TeamStat.objects.get(team=guest_team, league=league)
        except League.DoesNotExist as e:
            return HttpResponse(e.args[0], status=500)
        except Team.DoesNotExist as e:
            return HttpResponse(e.args[0], status=500)
        except TeamStat.DoesNotExist as e:
            return HttpResponse(e.args[0], status=500)

        try:
            add_points_to_team(home_stat, home_score, guest_score)
            add_points_to_team(guest_stat, guest_score, home_score)
        except Exception as e:
            return HttpResponse("[!] Score process error! " + e.args[0])

        try:
            match = Match.objects.create(team_home=home_stat, team_guest=guest_stat, team_home_goals=home_score,
                                         team_guest_goals=guest_score)
            match.save()
            home_stat.save()
            guest_stat.save()
        except DatabaseError as e:
            return HttpResponse("[!] Database error! " + e.args[0], status=500)

        return HttpResponse("Match between " + home_team.name + " and " + guest_team.name + " is created")


class CreateTeam(View):
    """
    Handle AJAX request and create new team
    """
    def post(self, request):
        try:
            team_name = str(request.POST['team_name'])
            team_shortcut = str(request.POST['team_shortcut'])
            if not team_name or not team_shortcut:
                return HttpResponse("[!] Some of the request variables is empty", status=400)

        except MultiValueDictKeyError as e:
            return HttpResponse("[!] Value key error in " + e.args[0] + " while request!", status=400)

        if Team.objects.filter(name=team_name) or Team.objects.filter(shortcut=team_shortcut):
            return HttpResponse("Team " + team_name + " already exist!")

        try:
            team = Team.objects.create(name=team_name, shortcut=team_shortcut)
            team.save()
        except DatabaseError as e:
            return HttpResponse("[!] Database error! " + e.args[0], status=500)

        return HttpResponse('Team ' + team_name + ' is created!')


class CreatePlayer(View):
    """
    Handle AJAX request and create new player for specific team
    """
    def post(self, request):
        try:
            player_name = str(request.POST['player_name'])
            player_age = int(request.POST['player_age'])
            player_team = str(request.POST['player_team'])
            if not player_name or not player_age or not player_team:
                return HttpResponse("[!] Some of the request variables is empty", status=400)
        except MultiValueDictKeyError as e:
            return HttpResponse("[!] Value key error in " + e.args[0] + " while request!", status=400)
        except ValueError as e:
            return HttpResponse(e.args[0] + _("[!] Please enter number!"), status=400)

        try:
            team = Team.objects.get(name=player_team)
        except Team.DoesNotExist as e:
            return HttpResponse(e.args[0], status=500)

        if Player.objects.filter(team=team, name=player_name):
            return HttpResponse("[!] Player " + player_name + " already exist in " + player_team + "!")

        try:
            player = Player.objects.create(team=team, name=player_name, age=player_age)
            player.save()
        except DatabaseError as e:
            return HttpResponse("[!] Database error! " + e.args[0], status=500)

        return HttpResponse('Player ' + player_name + ' is created!')


class AddTeamToLeague(View):
    """
    Handle AJAX request and add specific team to league
    """
    def post(self, request):
        try:
            team_name = str(request.POST['team_name'])
            league_name = str(request.POST['league_name'])
            if not team_name or not league_name:
                return HttpResponse("[!] Some of the request variables is empty", status=400)
        except MultiValueDictKeyError as e:
            return HttpResponse("[!] Value key error in " + e.args[0] + " while request!", status=400)

        try:
            team = Team.objects.get(name=team_name)
            league = League.objects.get(shortcut=league_name)
        except League.DoesNotExist as e:
            return HttpResponse(e.args[0], status=500)
        except Team.DoesNotExist as e:
            return HttpResponse(e.args[0], status=500)

        if TeamStat.objects.filter(team=team, league=league):
            return HttpResponse("Team already play in this league")

        try:
            team_stat = TeamStat.objects.create(team=team, league=league)
            team_stat.save()
        except DatabaseError as e:
            return HttpResponse("[!] Database error! " + e.args[0], status=500)

        return HttpResponse("Team " + str(team_name) + " now in " + str(league_name))
