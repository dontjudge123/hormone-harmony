from django.contrib import admin
from .models import PeriodCycle


@admin.register(PeriodCycle)
class PeriodCycleAdmin(admin.ModelAdmin):
	list_display = ('user', 'start_date', 'cycle_length')
	list_filter = ('user',)
