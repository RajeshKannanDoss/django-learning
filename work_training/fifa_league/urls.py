# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views


app_name = "fifa_league"
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^create_league/', views.CreateLeague.as_view(), name='create_league'),
    url(r'^get_data/', views.GetData.as_view(), name='get_data'),
    url(r'^create_match/', views.CreateMatch.as_view(), name='create_match'),
    url(r'^create_team/', views.CreateTeam.as_view(), name='create_team'),
    url(r'^create_player/', views.CreatePlayer.as_view(), name='create_player'),
    url(r'^add_team_to_league/', views.AddTeamToLeague.as_view(), name='add_team_to_league'),
    url(r'^(?P<league_id>[0-9a-zA-Z]+)/$', views.TeamsListView.as_view(), name='league'),
    url(r'^(?P<league_id>[0-9a-zA-Z]+)/(?P<team_id>[0-9a-zA-Z]+)/$', views.TeamView.as_view(), name='team'),
]


