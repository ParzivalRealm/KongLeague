from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from .models import Team, MatchDay, Match, Tournament


# Public Views

def standings_view(request):
    """Main tournament standings page"""
    tournament = Tournament.get_current()
    teams = Team.objects.all()

    # Create standings list with calculated stats
    standings = []
    for team in teams:
        standings.append({
            'team': team,
            'wins': team.wins,
            'losses': team.losses,
            'total_matches': team.total_matches,
            'win_rate': team.win_rate
        })

    # Sort by wins (descending), then by win_rate
    standings.sort(key=lambda x: (x['wins'], x['win_rate']), reverse=True)

    # Get recent matches (last 5)
    recent_matches = Match.objects.filter(winner__isnull=False).order_by('-played_at', '-created_at')[:5]

    context = {
        'tournament': tournament,
        'standings': standings,
        'recent_matches': recent_matches,
    }
    return render(request, 'tournament/standings.html', context)


def schedule_view(request):
    """Tournament schedule page"""
    tournament = Tournament.get_current()
    match_days = MatchDay.objects.prefetch_related('matches__team_a', 'matches__team_b', 'matches__winner').all()

    context = {
        'tournament': tournament,
        'match_days': match_days,
    }
    return render(request, 'tournament/schedule.html', context)


def teams_view(request):
    """Teams list page"""
    tournament = Tournament.get_current()
    teams = Team.objects.all()

    # Add stats to each team
    teams_with_stats = []
    for team in teams:
        teams_with_stats.append({
            'team': team,
            'wins': team.wins,
            'losses': team.losses,
            'win_rate': team.win_rate
        })

    context = {
        'tournament': tournament,
        'teams': teams_with_stats,
    }
    return render(request, 'tournament/teams.html', context)


# Admin Views

def admin_login_view(request):
    """Custom login page for admins"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')

    return render(request, 'tournament/admin_login.html')


def admin_logout_view(request):
    """Logout view"""
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente')
    return redirect('standings')


@login_required
def dashboard_view(request):
    """Admin dashboard"""
    tournament = Tournament.get_current()
    teams = Team.objects.all()
    match_days = MatchDay.objects.all()
    total_matches = Match.objects.count()
    completed_matches = Match.objects.filter(winner__isnull=False).count()

    context = {
        'tournament': tournament,
        'teams': teams,
        'match_days': match_days,
        'total_matches': total_matches,
        'completed_matches': completed_matches,
    }
    return render(request, 'tournament/dashboard.html', context)


@login_required
def manage_teams_view(request):
    """Team management page"""
    teams = Team.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add':
            name = request.POST.get('name')
            logo_url = request.POST.get('logo_url')
            captain_name = request.POST.get('captain_name')

            if name:
                Team.objects.create(
                    name=name,
                    logo_url=logo_url or None,
                    captain_name=captain_name or None
                )
                messages.success(request, f'Equipo "{name}" creado exitosamente')
            else:
                messages.error(request, 'El nombre del equipo es requerido')

        elif action == 'delete':
            team_id = request.POST.get('team_id')
            team = get_object_or_404(Team, id=team_id)
            team_name = team.name
            team.delete()
            messages.success(request, f'Equipo "{team_name}" eliminado')

        elif action == 'edit':
            team_id = request.POST.get('team_id')
            team = get_object_or_404(Team, id=team_id)
            team.name = request.POST.get('name', team.name)
            team.logo_url = request.POST.get('logo_url') or None
            team.captain_name = request.POST.get('captain_name') or None
            team.save()
            messages.success(request, f'Equipo "{team.name}" actualizado')

        return redirect('manage_teams')

    context = {
        'teams': teams,
    }
    return render(request, 'tournament/manage_teams.html', context)


@login_required
def manage_matches_view(request):
    """Match management page"""
    match_days = MatchDay.objects.prefetch_related('matches').all()
    teams = Team.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add_match_day':
            day_number = request.POST.get('day_number')
            name = request.POST.get('name')
            date = request.POST.get('date') or None

            if day_number and name:
                MatchDay.objects.create(
                    day_number=day_number,
                    name=name,
                    date=date
                )
                messages.success(request, f'Jornada "{name}" creada')
            else:
                messages.error(request, 'Número de día y nombre son requeridos')

        elif action == 'add_match':
            match_day_id = request.POST.get('match_day_id')
            team_a_id = request.POST.get('team_a_id')
            team_b_id = request.POST.get('team_b_id')

            if match_day_id and team_a_id and team_b_id:
                if team_a_id == team_b_id:
                    messages.error(request, 'Un equipo no puede jugar contra sí mismo')
                else:
                    match_day = get_object_or_404(MatchDay, id=match_day_id)
                    team_a = get_object_or_404(Team, id=team_a_id)
                    team_b = get_object_or_404(Team, id=team_b_id)

                    Match.objects.create(
                        match_day=match_day,
                        team_a=team_a,
                        team_b=team_b
                    )
                    messages.success(request, f'Partido "{team_a.name} vs {team_b.name}" creado')
            else:
                messages.error(request, 'Todos los campos son requeridos')

        elif action == 'set_winner':
            match_id = request.POST.get('match_id')
            winner_id = request.POST.get('winner_id')

            if match_id and winner_id:
                match = get_object_or_404(Match, id=match_id)
                winner = get_object_or_404(Team, id=winner_id)

                if winner in [match.team_a, match.team_b]:
                    from django.utils import timezone
                    match.winner = winner
                    match.played_at = timezone.now()
                    match.save()
                    messages.success(request, f'Ganador registrado: {winner.name}')
                else:
                    messages.error(request, 'El ganador debe ser uno de los equipos del partido')
            else:
                messages.error(request, 'Información incompleta')

        elif action == 'delete_match':
            match_id = request.POST.get('match_id')
            match = get_object_or_404(Match, id=match_id)
            match.delete()
            messages.success(request, 'Partido eliminado')

        return redirect('manage_matches')

    context = {
        'match_days': match_days,
        'teams': teams,
    }
    return render(request, 'tournament/manage_matches.html', context)


@login_required
def tournament_settings_view(request):
    """Tournament settings page"""
    tournament = Tournament.get_current()
    teams = Team.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update_status':
            status = request.POST.get('status')
            if status in ['upcoming', 'in_progress', 'completed']:
                tournament.status = status
                tournament.save()
                messages.success(request, f'Estado del torneo actualizado a "{tournament.get_status_display()}"')

        elif action == 'set_champion':
            champion_id = request.POST.get('champion_id')
            if champion_id:
                champion = get_object_or_404(Team, id=champion_id)
                tournament.champion = champion
                tournament.status = 'completed'
                tournament.save()
                messages.success(request, f'¡{champion.name} es el campeón del torneo!')

        elif action == 'reset':
            # Clear all match results but keep teams and match days
            Match.objects.update(winner=None, played_at=None)
            tournament.champion = None
            tournament.status = 'upcoming'
            tournament.save()
            messages.success(request, 'Torneo reiniciado - todos los resultados han sido borrados')

        return redirect('tournament_settings')

    context = {
        'tournament': tournament,
        'teams': teams,
    }
    return render(request, 'tournament/tournament_settings.html', context)
