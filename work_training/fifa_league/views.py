from .models import League, Team, Match, TeamStat, Player
from django.views import generic, View
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


# Main view
class IndexView(generic.ListView):
    def get(self, request, *args, **kwargs):
        leagues_list = League.objects.all()
        teams = Team.objects.all()
        return render(request, 'leagues/leagues_list.html', {'leagues_list': leagues_list, 'teams': teams})


# Teams for league view
class TeamsView(View):
    def get(self, request, *args, **kwargs):
        teams = url_to_id(str(self.kwargs['league_id']), League).league.order_by("points").reverse()
        league = url_to_id(str(self.kwargs['league_id']), League)
        leagues_list = League.objects.all()
        return render(request, 'leagues/team_list.html', {'teams': teams, 'leagues_list': leagues_list, 'league':league})


class TeamView(View):
    def get(self, request, *args, **kwargs):
        league = League.objects.get(shortcut=self.kwargs['league_id'])
        leagues_list = League.objects.all()
        team = Team.objects.get(shortcut=self.kwargs['team_id'])
        team_stat = team.team.get(team=team, league=league)
        return render(request, 'teams/team_view.html', {'team': team, 'team_stat': team_stat, 'leagues_list': leagues_list})


def get_data(request):
    if request.is_ajax:
        action = request.POST['action']
        response = []
        response_data = {}
        if action == 'get_teams_list_from_league':
            try:
                league_shortcut = request.POST['league_shortcut']
                teams = League.objects.get(shortcut=league_shortcut).league.all()
                for team in teams:
                    response.append(team.team.name)
                response_data['teams_names'] = response
                return JsonResponse(response_data)
            except:
                return HttpResponse("[!] Error")
        elif action == 'get_teams_list':
            try:
                teams = Team.objects.all()
                for team in teams:
                    response.append(team.name)
                response_data['teams_names'] = response
                return JsonResponse(response_data)
            except:
                return HttpResponse("[!] Error while data getting")


class CreateLeague(View):
    def post(self, request, *args, **kwargs):
        try:
            league_name = str(request.POST['name'])
            league_shortcut = str(request.POST['shortcut'])
            if League.objects.filter(name=league_name, shortcut=league_shortcut):
                return HttpResponse("League " + league_name + " already exist!")
            league = League.objects.create(name=league_name, shortcut=league_shortcut)
            league.save()
            return HttpResponse("League " + league_name + " is create!")
        except:
            return HttpResponse("[!] Error")


class CreateMatch(View):
    def post(self, request, *args, **kwargs):
        win_point = 3
        draw_point = 1
        try:
            league = League.objects.get(shortcut=request.POST['league'])
            home_team = Team.objects.get(name=request.POST['home_team'])
            guest_team = Team.objects.get(name=request.POST['guest_team'])

            if home_team == guest_team:
                return HttpResponse("[!] Error - same team cannot play with each other!")

            home_stat = TeamStat.objects.get(team=home_team, league=league)
            guest_stat = TeamStat.objects.get(team=guest_team, league=league)
        except:
            return HttpResponse("[!] Object get error!")

        try:
            home_score = int(request.POST['home_score'])
            guest_score = int(request.POST['guest_score'])
        except:
            return HttpResponse("[!] Score handle error!")

        try:
            if home_score > guest_score:
                home_stat.points += win_point
                home_stat.wins += 1
                guest_stat.loses += 1
            elif home_score < guest_score:
                guest_stat.points += win_point
                guest_stat.wins += 1
                home_stat.loses += 1
            else:
                guest_stat.draws += draw_point
                home_stat.draws += draw_point
                guest_stat.points += 1
                home_stat.points += 1

            home_stat.match_count += 1
            guest_stat.match_count += 1
            home_stat.goals_scored += home_score
            guest_stat.goals_scored += guest_score
            home_stat.goals_conceded += guest_score
            guest_stat.goals_conceded += home_score
        except:
            return HttpResponse("[!] Score process error!")

        try:
            match = Match.objects.create(team_home=home_stat, team_guest=guest_stat, team_home_goals=home_score, team_guest_goals=guest_score)
            match.save()
            home_stat.save()
            guest_stat.save()
        except:
            return HttpResponse("[!] Save or create objects error!")
        return HttpResponse("Match between " + home_team.name + " and " + guest_team.name + " is created")


# create team AJAX handle
class CreateTeam(View):
    def post(self, request, *args, **kwargs):
        try:
            team_name = request.POST['team_name']
            team_shortcut = request.POST['team_shortcut']
            if Team.objects.filter(name=team_name, shortcut=team_shortcut):
                return HttpResponse("Team " + team_name + " already exist!")
            team = Team.objects.create(name=team_name, shortcut=team_shortcut)
            team.save()
            return HttpResponse('Team ' + team_name + ' is created!')
        except:
            return HttpResponse('[!] Team creation error!')


class CreatePlayer(View):
    def post(self, request, *args, **kwargs):
        try:
            player_name = request.POST['player_name']
            player_age = request.POST['player_age']
            player_team = request.POST['player_team']
            team = Team.objects.get(name=player_team)
            if Player.objects.filter(team=team, name=player_name):
                return HttpResponse("[!] Player " + player_name + " already exist in " + player_team + "!")
            player = Player.objects.create(team=team, name=player_name, age=player_age)
            player.save()
            return HttpResponse('Player ' + player_name + ' is created!')
        except:
            return HttpResponse('[!] Player create - error')


class AddTeamToLeague(View):
    def post(self, request):
        try:
            team_name = request.POST['team_name']
            league_name = request.POST['league_name']
            team = Team.objects.get(name=team_name)
            league = League.objects.get(shortcut=league_name)
            if TeamStat.objects.filter(team=team, league=league):
                return HttpResponse("Team already play in this league")
            team_stat = TeamStat.objects.create(team=team, league=league)
            team_stat.save()
            return HttpResponse("Team " + str(team_name) + " now in " + str(league_name))
        except:
            return HttpResponse("[!] Error")


# need to refact
def url_to_id(url, model):
    return model.objects.get(shortcut=url)
