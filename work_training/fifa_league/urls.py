"""
URL pattern file for fifa_league app
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from . import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r'user', views.UserViewSet, base_name='user')
router.register(r'teams', views.TeamViewSet, base_name='teams')
router.register(r'leagues', views.LeagueList.as_view(), base_name='leagues')

app_name = "fifa_league"
urlpatterns = [
    # API url
    url(r'^api/leagues/$', views.LeagueList.as_view()),
    url(r'^api/', include(router.urls)),

    url(r'^$', views.IndexView.as_view(), name='index'),

    # user views urls
    url(r'^logout_user', views.LogOutUserView.as_view(), name='logout_user'),
    url(r'^login_user/', views.LoginUserView.as_view(), name='login_user'),
    url(r'^create_user/', views.CreateUserView.as_view(), name='create_user'),
    url(r'^user/(?P<username>[0-9a-zA-Z]+)/settings',
        views.UserSettingsView.as_view(), name='user_settings'),

    # uploads
    url(r'^avatar_upload/$', views.UserAvatarUploadView.as_view(),
        name='avatar_upload'),

    url(r'^create_league/', views.CreateLeagueView.as_view(),
        name='create_league'),
    url(r'^create_match/', views.CreateMatchView.as_view(),
        name='create_match'),
    url(r'^create_team/', views.CreateTeamView.as_view(),
        name='create_team'),
    url(r'^create_player/', views.CreatePlayerView.as_view(),
        name='create_player'),
    url(r'^create_teamstat/', views.CreateTeamStatView.as_view(),
        name='create_teamstat'),
    url(r'^(?P<league_shortcut>[0-9a-zA-Z]+)/$',
        views.TeamsListView.as_view()),

    url(r'^(?P<league_shortcut>[0-9a-zA-Z]+)'
        r'/(?P<team_shortcut>[0-9a-zA-Z]+)/$', views.TeamView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
