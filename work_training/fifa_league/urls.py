from django.conf.urls import url

from . import views

app_name = "fifa_league"
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^addmenu/', views.AddMenu.as_view(), name='add_menu'),
    url(r'^(?P<league_id>[0-9a-zA-Z]+)/$', views.TeamsView.as_view(), name='league'),
    #url(r'^[0-9a-zA-Z]+/create_team/$', views.CreateTeam.as_view(), name='create_match'),
    #url(r'^(?P<league_id>[0-9a-zA-Z]+)/create_match/$', views.CreateMatch.as_view(), name='create_match'),
    url(r'^(?P<league_id>[0-9a-zA-Z]+)/(?P<team_id>[0-9a-zA-Z]+)/$', views.TeamView.as_view(), name='league'),
]
