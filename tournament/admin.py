from django.contrib import admin
from .models import Team, MatchDay, Match, Tournament


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'captain_name', 'created_at']
    search_fields = ['name', 'captain_name']
    list_filter = ['created_at']


@admin.register(MatchDay)
class MatchDayAdmin(admin.ModelAdmin):
    list_display = ['name', 'day_number', 'date']
    ordering = ['day_number']


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['match_day', 'team_a', 'team_b', 'winner', 'played_at']
    list_filter = ['match_day', 'winner']
    search_fields = ['team_a__name', 'team_b__name']
    raw_id_fields = ['team_a', 'team_b', 'winner']


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'champion', 'created_at']
    list_filter = ['status']
