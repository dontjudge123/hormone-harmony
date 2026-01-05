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
