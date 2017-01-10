"""
forms.py - contains Django work classes to generate and validate forms
"""

from django.contrib.auth.models import User
from django import forms

from .models import League, Team, Player, TeamStat, Match


class UserCreateForm(forms.ModelForm):
    """
    User Form for registration and next login new user
    """
    password = forms.CharField(widget=forms.PasswordInput)
    username = forms.SlugField()
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class UserLoginForm(forms.Form):
    """
    Form for login user
    """
    username = forms.SlugField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserChangePasswordForm(forms.Form):
    """
    Form to change user password
    """
    old_password = forms.CharField(widget=forms.PasswordInput,
                                   label='Old password')
    new_password1 = forms.CharField(widget=forms.PasswordInput,
                                    label='New password')
    new_password2 = forms.CharField(widget=forms.PasswordInput,
                                    label='New password (one more time)')


class UserChangeEmailForm(forms.Form):
    """
    Form for user email change
    """
    new_email = forms.EmailField(label='New email')


class LeagueCreateForm(forms.ModelForm):
    """
    Form for League create
    """
    name = forms.CharField()
    shortcut = forms.SlugField(widget=forms.TextInput(
        attrs={'pattern': '[A-Za-z0-9]+'}))

    class Meta:
        model = League
        fields = ('name', 'shortcut',)


class TeamCreateForm(forms.ModelForm):
    """
    Form for Team create
    """
    name = forms.CharField()
    shortcut = forms.SlugField(widget=forms.TextInput(
        attrs={'pattern': '[A-Za-z0-9]+'}))

    class Meta:
        model = Team
        fields = ('name', 'shortcut',)


class PlayerCreateForm(forms.ModelForm):
    """
    Form for Player create
    """
    team = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        empty_label=None,
        to_field_name='shortcut')
    name = forms.CharField()
    age = forms.IntegerField(min_value=1, max_value=200)

    class Meta:
        model = Player
        fields = ('team', 'name', 'age',)


class TeamStatCreateForm(forms.ModelForm):
    """
    Form for add Team to League
    - this form cretae TeamStat for specific Team and League
    """
    team = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        empty_label=None,
        to_field_name='shortcut')
    league = forms.ModelChoiceField(
        queryset=League.objects.all(),
        empty_label=None,
        to_field_name='shortcut')

    class Meta:
        model = TeamStat
        fields = ('team', 'league',)


class ChoiceFieldNoValidation(forms.ChoiceField):
    """
    Custom Choice field without validate
    """
    def validate(self, value):
        return True


class MatchCreateForm(forms.Form):
    """
    Form for create matches
    """

    league = forms.ModelChoiceField(queryset=League.objects.all(),
                                    empty_label=None,
                                    to_field_name='shortcut')
    team_home = ChoiceFieldNoValidation()
    team_home_goals = forms.IntegerField(min_value=0)
    team_guest = ChoiceFieldNoValidation()
    team_guest_goals = forms.IntegerField(min_value=0)

    def create(self):
        league_shortcut = self['league'].data
        team_home_shortcut = self['team_home'].data
        team_guest_shortcut = self['team_guest'].data
        team_home_goals = int(self['team_home_goals'].data)
        team_guest_goals = int(self['team_guest_goals'].data)

        try:
            league = League.objects.get(shortcut=league_shortcut)
            home_team = Team.objects.get(shortcut=team_home_shortcut)
            guest_team = Team.objects.get(shortcut=team_guest_shortcut)

            if home_team == guest_team:
                raise ValueError

            home_stat = TeamStat.objects.get(team=home_team, league=league)
            guest_stat = TeamStat.objects.get(team=guest_team, league=league)
        except League.DoesNotExist:
            raise ValueError("League object doesn't exist!")
        except Team.DoesNotExist:
            raise ValueError("Team object doesn't exist!")
        except TeamStat.DoesNotExist:
            raise ValueError("League object doesn't exist!")

        match = Match.objects.create(team_home=home_stat,
                                     team_guest=guest_stat,
                                     team_home_goals=team_home_goals,
                                     team_guest_goals=team_guest_goals)
        return match
