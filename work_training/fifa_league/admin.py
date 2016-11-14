from django.contrib import admin

# Register your models here.
from .models import League, Team, Player, Match, TeamStat

admin.site.register(League)
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Match)
admin.site.register(TeamStat)