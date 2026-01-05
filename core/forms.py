from django import forms
from .models import PeriodCycle


class PeriodCycleForm(forms.ModelForm):
    # allow users to optionally provide an end_date; it won't be saved but will compute cycle_length
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    # cycle_length can be optional if user provides end_date
    cycle_length = forms.IntegerField(required=False, min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1}))

    class Meta:
        model = PeriodCycle
        fields = ["start_date", "cycle_length"]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'cycle_length': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
        labels = {
            'start_date': 'Start date',
            'cycle_length': 'Cycle length (days)'
        }
        help_texts = {
            'cycle_length': 'Typical cycle length in days (e.g., 28)'
        }

    def clean(self):
        cleaned = super().clean()
        start = cleaned.get('start_date')
        end = cleaned.get('end_date')
        length = cleaned.get('cycle_length')

        if start and end:
            # inclusive difference
            delta = (end - start).days + 1
            if delta <= 0:
                raise forms.ValidationError('End date must be on or after start date')
            # if cycle_length not provided or inconsistent, set it
            if not length or length != delta:
                cleaned['cycle_length'] = delta

        return cleaned
