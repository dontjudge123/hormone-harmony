from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PeriodCycleForm
from .models import PeriodCycle
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
