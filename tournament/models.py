from django.db import models
from django.core.validators import MinValueValidator


class Team(models.Model):
    """Represents a tournament team"""
    name = models.CharField(max_length=100, unique=True)
    logo_url = models.URLField(blank=True, null=True)
    captain_name = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def wins(self):
        """Count total wins for this team"""
        return Match.objects.filter(winner=self).count()

    @property
    def losses(self):
        """Count total losses for this team"""
        return Match.objects.filter(
            models.Q(team_a=self) | models.Q(team_b=self),
            winner__isnull=False
        ).exclude(winner=self).count()

    @property
    def total_matches(self):
        """Count total matches played"""
        return Match.objects.filter(
            models.Q(team_a=self) | models.Q(team_b=self),
            winner__isnull=False
        ).count()

    @property
    def win_rate(self):
        """Calculate win rate percentage"""
        if self.total_matches == 0:
            return 0
        return round((self.wins / self.total_matches) * 100, 1)


class MatchDay(models.Model):
    """Represents a day/round in the tournament"""
    day_number = models.IntegerField(validators=[MinValueValidator(1)], unique=True)
    date = models.DateField(blank=True, null=True)
    name = models.CharField(max_length=100, help_text="e.g., 'Jornada 1'")

    class Meta:
        ordering = ['day_number']

    def __str__(self):
        return f"{self.name} (Day {self.day_number})"


class Match(models.Model):
    """Represents a match between two teams"""
    match_day = models.ForeignKey(MatchDay, on_delete=models.CASCADE, related_name='matches')
    team_a = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches_as_team_a')
    team_b = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches_as_team_b')
    winner = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_matches')
    played_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['match_day__day_number', 'created_at']
        verbose_name_plural = "Matches"

    def __str__(self):
        winner_text = f" (Ganador: {self.winner.name})" if self.winner else ""
        return f"{self.team_a.name} vs {self.team_b.name}{winner_text}"

    def clean(self):
        """Validate that team_a and team_b are different"""
        from django.core.exceptions import ValidationError
        if self.team_a == self.team_b:
            raise ValidationError("Un equipo no puede jugar contra sí mismo")
        if self.winner and self.winner not in [self.team_a, self.team_b]:
            raise ValidationError("El ganador debe ser uno de los equipos que juega")


class Tournament(models.Model):
    """Represents the tournament settings and status"""
    STATUS_CHOICES = [
        ('upcoming', 'Próximo'),
        ('in_progress', 'En Progreso'),
        ('completed', 'Completado'),
    ]

    name = models.CharField(max_length=200, default="KongLeague Aram chaos")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    champion = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='championships')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"

    @classmethod
    def get_current(cls):
        """Get or create the current tournament"""
        tournament, created = cls.objects.get_or_create(
            status__in=['upcoming', 'in_progress'],
            defaults={'name': 'KongLeague Aram chaos'}
        )
        return tournament
