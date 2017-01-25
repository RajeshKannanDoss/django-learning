"""
admin.py - config file for Django admin panel
"""
from django.contrib import admin
from .models import League, Team, Player, TeamStat, Match


admin.site.site_title = "Football App"
admin.site.site_header = "FIFA Leagues App"
admin.site.index_title = 'FIFA App'


class HomeMatchInline(admin.TabularInline):
    """
    Home Match class for add to TeamStat inline
    """
    model = Match
    fk_name = "team_home"


class GuestMatchInline(admin.TabularInline):
    """
    Guest Match class for add to TeamStat inline
    """
    model = Match
    fk_name = "team_guest"


class PlayerInline(admin.StackedInline):
    """
    Stacked Inline class for Player model
    """
    model = Player


class TeamStatToLeagueInline(admin.TabularInline):
    """
    Tabular Inline class for TeamStat model with foreign key connect to league
    """
    model = TeamStat
    fk_name = 'league'


class TeamAdmin(admin.ModelAdmin):
    """
    Add PlayerInline to Team inlines in Django admin
    Display:
    - Team name column

    Inlines:
    - Player model connected to this Team
    """
    list_display = ['name']
    inlines = [
        PlayerInline,
    ]


class TeamStatAdmin(admin.ModelAdmin):
    """
    Config class for TeamStat display in Django admin
    Display:
    - __str__ name like in Models
    - points

    Add filter by:
    - leagues

    Order - order by points, from max to min
    Inlines:
    - HomeMatches connected to this TeamStat
    - GuestMatches connected to this TeamStat
    """
    list_display = ['__str__', 'points']
    list_filter = ['league']
    ordering = ['-points']
    inlines = [
        HomeMatchInline, GuestMatchInline
    ]


class LeagueAdmin(admin.ModelAdmin):
    """
    Add TeamStatToLeagueInline to League inlines in Django admin
    Search by:
    - name
    - shortcut

    Inlines:
    - TeamStats connected to this League
    """
    search_fields = ['name', 'shortcut']
    inlines = [
        TeamStatToLeagueInline,
    ]


class PlayerAdmin(admin.ModelAdmin):
    """
    Player model for Django admin
    Display:
    - name column

    Search by:
    - name

    Add filter by:
    - teams
    """
    list_display = ['name']
    search_fields = ['name']
    list_filter = ['team']


admin.site.register(League, LeagueAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(TeamStat, TeamStatAdmin)
