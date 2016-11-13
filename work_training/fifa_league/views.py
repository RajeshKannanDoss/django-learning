from .models import League, Team, Match
from django.views import generic, View
from django.http import HttpResponseRedirect
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
        teams = url_to_id(str(self.kwargs['league_id']), League).team_set.order_by("points").reverse()
        leagues_list = League.objects.all()
        return render(request, 'leagues/team_list.html', {'teams': teams, 'leagues_list': leagues_list})


class TeamView(generic.ListView):
    template_name = 'teams/team_view.html'
    context_object_name = 'team'

    def get_queryset(self):
        object = League.objects.get(shortcut=self.kwargs['league_id'])
        return object.team_set.get(shortcut=self.kwargs['team_id'])


class CreateMatch(View):
    def post(self, request, *args, **kwargs):
        win_point = 3
        draw_point = 1
        home_team = url_to_id(request.POST['home_team'], Team)
        guest_team = url_to_id(request.POST['guest_team'], Team)

        if home_team == guest_team:
            return HttpResponseRedirect("/fifa/")

        home_score = int(request.POST['home_score'])
        guest_score = int(request.POST['guest_score'])
        if home_score > guest_score:
            home_team.points += win_point
            home_team.wins += 1
            guest_team.loses += 1
        elif home_score < guest_score:
            guest_team.points += win_point
            guest_team.wins += 1
            home_team.loses += 1
        else:
            guest_team.draws += draw_point
            home_team.draws += draw_point
            guest_team.points += 1
            home_team.points += 1

        home_team.match_count += 1
        guest_team.match_count += 1
        home_team.goals_scored += home_score
        guest_team.goals_scored += guest_score
        home_team.goals_conceded += guest_score
        guest_team.goals_conceded += home_score

        match = Match.objects.create(team_home=home_team, team_guest=guest_team, team_home_goals=home_score, team_guest_goals=guest_score)
        match.save()
        home_team.save()
        guest_team.save()
        return HttpResponseRedirect('/fifa/' + self.kwargs['league_id'])


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
