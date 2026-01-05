from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator
from datetime import timedelta, datetime


class PeriodCycle(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    start_date = models.DateField()
    cycle_length = models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.user} - {self.start_date}"

    @property
    def end_date(self):
        """Compute the inclusive end date for this cycle."""
        start = self.start_date
        if isinstance(start, str):
            # defensive: parse if a string got stored
            start = datetime.strptime(start, "%Y-%m-%d").date()
        return start + timedelta(days=self.cycle_length - 1)


class Symptom(models.Model):
    cycle = models.ForeignKey(PeriodCycle, on_delete=models.CASCADE, related_name='symptoms')
    date = models.DateField()
    mood_choices = [
        ('Happy', 'Happy'),
        ('Sad', 'Sad'),
        ('Anxious', 'Anxious'),
        ('Tired', 'Tired'),
        ('Irritable', 'Irritable'),
    ]
    mood = models.CharField(max_length=20, choices=mood_choices)
    cramps = models.IntegerField(default=0)  # scale 0-10
    energy = models.IntegerField(default=5)  # scale 0-10

    def __str__(self):
        return f"{self.date} - {self.mood}"
