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


