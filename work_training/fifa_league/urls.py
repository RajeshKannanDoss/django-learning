from django.conf.urls import url

from . import views

app_name = "fifa_league"
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^create_league/', views.CreateLeague.as_view(), name='create_league'),
    url(r'^get_data/', views.get_data, name='get_data'),
    url(r'^create_match/', views.CreateMatch.as_view(), name='create_match'),
    url(r'^(?P<league_id>[0-9a-zA-Z]+)/$', views.TeamsView.as_view(), name='league'),
    url(r'^(?P<league_id>[0-9a-zA-Z]+)/(?P<team_id>[0-9a-zA-Z]+)/$', views.TeamView.as_view(), name='team'),
]
