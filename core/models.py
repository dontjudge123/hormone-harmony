from django.conf import settings
from django.db import models

class PeriodCycle(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    start_date = models.DateField()
    cycle_length = models.IntegerField()

    def __str__(self):
        return f"{self.user} - {self.start_date}"


