"""
File that contains mixins for Django fifa_league app
"""

from .forms import UserCreateForm, LeagueCreateForm, TeamCreateForm, \
    PlayerCreateForm, TeamStatCreateForm, MatchCreateForm, UserLoginForm


class UserFormsMixin:
    """
    Mixin for forms variables in template
    """
    def get_context_data(self, **kwargs):
        """
        :param kwargs:
        :return: forms for template
        """
        ctx = super().get_context_data(**kwargs)
        ctx.update(
            {
             'user_create_form': UserCreateForm(),
             'user_login_form': UserLoginForm(),
             'league_create_form': LeagueCreateForm(),
             'team_create_form': TeamCreateForm(),
             'player_create_form': PlayerCreateForm(),
             'teamstat_create_form': TeamStatCreateForm(),
             'match_create_form': MatchCreateForm()
            }
        )
        return ctx
