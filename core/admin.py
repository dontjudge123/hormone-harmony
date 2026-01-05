from django.contrib import admin
from .models import PeriodCycle, Symptom


@admin.register(PeriodCycle)
class PeriodCycleAdmin(admin.ModelAdmin):
	list_display = ('user', 'start_date', 'cycle_length')
	list_filter = ('user',)


@admin.register(Symptom)
class SymptomAdmin(admin.ModelAdmin):
	list_display = ('cycle', 'date', 'mood', 'cramps', 'energy')
	list_filter = ('mood',)
