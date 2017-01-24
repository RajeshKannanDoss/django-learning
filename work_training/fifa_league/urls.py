"""
URL pattern file for fifa_league app
"""
from django.conf.urls import url, include
from . import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r'user', views.UserViewSet, base_name='user')
router.register(r'teams', views.TeamViewSet, base_name='teams')
router.register(r'leagues', views.LeagueViewSet, base_name='leagues')
router.register(r'teamstat', views.TeamStatViewSet, base_name='teamstat')
router.register(r'match', views.MatchViewSet, base_name='match')
router.register(r'players', views.PlayerViewSet, base_name='players')

app_name = "fifa_league"
urlpatterns = [
    # API url
    url(r'^api/', include(router.urls)),

    url(r'^$', views.IndexView.as_view(), name='index'),

    # user views urls
    url(r'^logout_user', views.LogOutUserView.as_view(), name='logout_user'),
    url(r'^login_user/', views.LoginUserView.as_view(), name='login_user'),
    url(r'^create_user/', views.CreateUserView.as_view(), name='create_user'),
]
