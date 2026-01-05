from django import forms
from .models import PeriodCycle

class PeriodCycleForm(forms.ModelForm):
    class Meta:
        model = PeriodCycle
        fields = ["start_date", "cycle_length"]
