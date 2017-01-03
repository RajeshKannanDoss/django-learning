"""
URL pattern file for fifa_league app
"""
from django.conf.urls import url, include
from . import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r'teams', views.TeamViewSet, base_name='teams')
router.register(r'leagues', views.LeagueList.as_view(), base_name='leagues')

app_name = "fifa_league"
urlpatterns = [
    # API url
    url(r'api/leagues/$', views.LeagueList.as_view()),
    url(r'api/', include(router.urls)),
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^create_league/', views.CreateLeagueView.as_view()),
    url(r'^create_match/', views.CreateMatchView.as_view()),
    url(r'^create_team/', views.CreateTeamView.as_view()),
    url(r'^create_player/', views.CreatePlayerView.as_view()),
    url(r'^add_team_to_league/', views.AddTeamToLeagueView.as_view()),
    url(r'^(?P<league_shortcut>[0-9a-zA-Z]+)/$',
        views.TeamsListView.as_view()),

    url(r'^(?P<league_shortcut>[0-9a-zA-Z]+)'
        r'/(?P<team_shortcut>[0-9a-zA-Z]+)/$', views.TeamView.as_view()),
]
