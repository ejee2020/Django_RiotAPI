from django.contrib import admin
from .models import *
# Register your models here.


class ChampionAdmin(admin.ModelAdmin):
    list_display = ['Name', 'Num_played', 'Summoner']


admin.site.register(Champion, ChampionAdmin)


class SummonerAdmin(admin.ModelAdmin):
    list_display = ['Name', 'Num_played']


admin.site.register(Summoner, SummonerAdmin)


class MatchAdmin(admin.ModelAdmin):
    list_display = ['Match_id', 'Min_played']

    class Meta:
        verbose_name_plural = "matches"


admin.site.register(Match, MatchAdmin)


class MatchChampionAdmin(admin.ModelAdmin):
    list_display = ['Match_id', 'Min_played']


admin.site.register(Match_Champion, MatchChampionAdmin)
