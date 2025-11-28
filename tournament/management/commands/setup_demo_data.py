from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tournament.models import Team, MatchDay, Match, Tournament


class Command(BaseCommand):
    help = 'Load demo data for KongLeague tournament'

    def handle(self, *args, **kwargs):
        self.stdout.write('Setting up KongLeague demo data...\n')

        # Create superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@kongleague.com',
                password='admin123'
            )
            self.stdout.write(self.style.SUCCESS('✓ Superuser created (username: admin, password: admin123)'))
        else:
            self.stdout.write(self.style.WARNING('⚠ Superuser already exists'))

        # Create tournament
        tournament, created = Tournament.objects.get_or_create(
            name='KongLeague Season 1',
            defaults={'status': 'in_progress'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Tournament created'))
        else:
            self.stdout.write(self.style.WARNING('⚠ Tournament already exists'))

        # Create teams
        team_names = [
            'Las ratas',
            'FA1',
            'Papois',
            'Guaro Squad',
            'FA2',
            'FA3',
            'The Uwu Team',
            'Cascaras Blanca',
            'Los 9',
        ]

        teams = []
        for team_name in team_names:
            team, created = Team.objects.get_or_create(name=team_name)
            teams.append(team)
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Team created: {team_name}'))

        if Team.objects.count() == len(team_names):
            self.stdout.write(self.style.SUCCESS(f'\n✓ All {len(team_names)} teams ready'))

        # Create match days
        match_days_data = [
            {'day_number': 1, 'name': 'Jornada 1'},
            {'day_number': 2, 'name': 'Jornada 2'},
            {'day_number': 3, 'name': 'Jornada 3'},
        ]

        match_days = []
        for md_data in match_days_data:
            md, created = MatchDay.objects.get_or_create(
                day_number=md_data['day_number'],
                defaults={'name': md_data['name']}
            )
            match_days.append(md)
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Match day created: {md_data["name"]}'))

        # Create some sample matches for Jornada 1
        if match_days and len(teams) >= 6:
            matches_data = [
                (teams[0], teams[1]),  # Los Monos Furiosos vs Banana Diff
                (teams[2], teams[3]),  # Kong's Disciples vs Plátano Gaming
                (teams[4], teams[5]),  # Gorilla Warfare vs La Manada
            ]

            for team_a, team_b in matches_data:
                match, created = Match.objects.get_or_create(
                    match_day=match_days[0],
                    team_a=team_a,
                    team_b=team_b
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'✓ Match created: {team_a.name} vs {team_b.name}'))

        self.stdout.write(self.style.SUCCESS('\n🦍 KongLeague demo data setup complete! 🍌'))
        self.stdout.write(self.style.SUCCESS('\nYou can now:'))
        self.stdout.write(self.style.SUCCESS('1. Run the server: python manage.py runserver'))
        self.stdout.write(self.style.SUCCESS('2. Visit http://localhost:8000 for the public view'))
        self.stdout.write(self.style.SUCCESS('3. Login at http://localhost:8000/admin-login/ (admin/admin123)'))
        self.stdout.write(self.style.SUCCESS('\n¡Muestra tu fuerza! 💪'))
