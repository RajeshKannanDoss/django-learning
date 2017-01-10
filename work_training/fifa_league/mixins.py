"""
File that contains mixins for Django fifa_league app
"""

from .forms import UserCreateForm, LeagueCreateForm, TeamCreateForm, \
    PlayerCreateForm, TeamStatCreateForm, MatchCreateForm, UserLoginForm
from django.http import HttpResponse, HttpResponseForbidden, \
    HttpResponseBadRequest


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


class AjaxCheckMixin:
    """
    Mixin for check if request is Ajax

    NOTE:
        - mixin should be the left-corner of a view
    """
    def dispatch(self, request, *args, **kwargs):
        """
        Handle mixin functionality
        """
        if not request.is_ajax:
            return HttpResponseBadRequest('AJAX is required!')

        return super(AjaxCheckMixin, self).dispatch(request,
                                                    *args,
                                                    **kwargs)


class UserAuthenticationCheckMixin:
    """
    Mixin for check if user is authenticated

    NOTE:
        - mixin should be left-most mixin
        (instead of case when you use AjaxCheckMixin)
    """
    def dispatch(self, request, *args, **kwargs):
        """
        Handle mixin functionality
        """
        if not request.user.is_authenticated:
            return HttpResponse(status=401)

        return super(UserAuthenticationCheckMixin, self).dispatch(request,
                                                                  *args,
                                                                  **kwargs)


class UserPermissionsCheckMixin:
    """
    Mixin for check if user have necessary permissions

    variables:
        app_name - default 'fifa_league'
        permissions_required - list of required permissions,
        if permission doesn't exist HttpResponseForbidden will be return
    """
    permissions_required = []
    app_name = 'fifa_league'

    def dispatch(self, request, *args, **kwargs):
        """
        Handle mixin functionality
        """

        for perm in self.permissions_required:
            if not request.user.has_perm('{}.{}'.format(self.app_name, perm)):
                return HttpResponseForbidden()

        return super(UserPermissionsCheckMixin, self).dispatch(request,
                                                               *args,
                                                               **kwargs)
