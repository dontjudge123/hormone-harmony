from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PeriodCycleForm, SymptomForm
from .models import PeriodCycle, Symptom
from datetime import timedelta


@login_required
def period_tracker(request):
    if request.method == 'POST':
        form = PeriodCycleForm(request.POST)
        if form.is_valid():
            period = form.save(commit=False)
            period.user = request.user
            period.save()
            messages.success(request, 'Period cycle saved.')
            return redirect(reverse('core:period'))
    else:
        form = PeriodCycleForm()

    # show recent cycles for the logged in user
    cycles = PeriodCycle.objects.filter(user=request.user).order_by('-start_date')[:10]

    # basic prediction: take the most recent start date and add its cycle_length days
    from datetime import timedelta
    predicted_next_period = None
    last = cycles.first()
    if last:
        predicted_next_period = (last.start_date + timedelta(days=last.cycle_length)).isoformat()

    return render(request, "period_tracker.html", {'form': form, 'cycles': cycles, 'predicted_next_period': predicted_next_period})

@login_required
def symptom_tracker(request, cycle_id):
    cycle = get_object_or_404(PeriodCycle, id=cycle_id, user=request.user)
    if request.method == "POST":
        form = SymptomForm(request.POST)
        if form.is_valid():
            symptom = form.save(commit=False)
            symptom.cycle = cycle
            symptom.save()
            return redirect('core:symptom_tracker', cycle_id=cycle.id)
    else:
        form = SymptomForm()

    symptoms = cycle.symptoms.order_by('-date')
    return render(request, 'symptom_tracker.html', {'cycle': cycle, 'form': form, 'symptoms': symptoms})

from django.db.models import Avg
from django.core.serializers.json import DjangoJSONEncoder
import json

@login_required
def cycle_dashboard(request, cycle_id):
    cycle = get_object_or_404(PeriodCycle, id=cycle_id, user=request.user)
    symptoms = cycle.symptoms.order_by('date')

    # Prepare data for charts
    dates = [symptom.date.strftime("%Y-%m-%d") for symptom in symptoms]
    cramps = [symptom.cramps for symptom in symptoms]
    energy = [symptom.energy for symptom in symptoms]

    # Mood count
    mood_counts = {}
    for mood_choice in Symptom._meta.get_field('mood').choices:
        mood_counts[mood_choice[0]] = symptoms.filter(mood=mood_choice[0]).count()

    # Prepare a single JSON payload for client-side charts to avoid raw template injection in JS
    chart_payload = {
        'dates': dates,
        'cramps': cramps,
        'energy': energy,
        'mood_counts': mood_counts,
    }

    context = {
        'cycle': cycle,
        'dates': json.dumps(dates, cls=DjangoJSONEncoder),
        'cramps': json.dumps(cramps),
        'energy': json.dumps(energy),
        'mood_counts': json.dumps(mood_counts),
        'chart_data_json': json.dumps(chart_payload, cls=DjangoJSONEncoder),
    }
    return render(request, 'core/cycle_dashboard.html', context)
