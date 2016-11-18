from .models import League, Team, Match, TeamStat
from django.views import generic, View
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
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
        return render(request, 'leagues/team_list.html', {'teams': teams, 'league': league})


class TeamView(View):
    def get(self, request, *args, **kwargs):
        league = League.objects.get(shortcut=self.kwargs['league_id'])
        team = Team.objects.get(shortcut=self.kwargs['team_id'])
        team_stat = team.team.get(team=team, league=league)
        return render(request, 'teams/team_view.html', {'team': team, 'team_stat': team_stat})


def get_data(request):
    if request.is_ajax:
        action = request.POST['action']
        if action == 'get_teams_list_from_league':
            try:
                league_shortcut = request.POST['league_shortcut']
                teams = League.objects.get(shortcut=league_shortcut).league.all()
                response = []
                response_data = {}
                for team in teams:
                    response.append(team.team.name)
                response_data['teams_names'] = response
                return JsonResponse(response_data)
            except:
                return HttpResponse("[!] Error")

class CreateLeague(View):
    def post(self, request, *args, **kwargs):
        try:
            league_name = str(request.POST['name'])
            league_shortcut = str(request.POST['shortcut'])
            league = League.objects.create(name=league_name, shortcut=league_shortcut)
            league.save()
            return HttpResponse("League" + league_name)
        except:
            return HttpResponse("[!] Error")


class CreateMatch(View):
    def post(self, request, *args, **kwargs):
        win_point = 3
        draw_point = 1
        league = League.objects.get(shortcut=request.POST['league'])
        home_team = Team.objects.get(name=request.POST['home_team'])
        guest_team = Team.objects.get(name=request.POST['guest_team'])

        if home_team == guest_team:
            return HttpResponse("[!] Error")

        home_score = int(request.POST['home_score'])
        guest_score = int(request.POST['guest_score'])

        home_stat = TeamStat.objects.get(team=home_team, league=league)
        guest_stat = TeamStat.objects.get(team=guest_team, league=league)
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

        match = Match.objects.create(team_home=home_stat, team_guest=guest_stat, team_home_goals=home_score, team_guest_goals=guest_score)
        match.save()
        home_stat.save()
        guest_stat.save()
        return HttpResponse("All work!")


# Not in use
class CreateTeam(View):
    def post(self, request, *args, **kwargs):
        league = url_to_id(request.POST['league_name'], League)
        team_name = request.POST['team_name']
        team_shortcut = request.POST['team_shortcut']
        team = Team.objects.create(league=league, name=team_name, shortcut=team_shortcut)
        team.save()
        return HttpResponseRedirect('/fifa/')


def url_to_id(url, model):
    return model.objects.get(shortcut=url)
