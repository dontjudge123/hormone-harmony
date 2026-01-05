from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PeriodCycleForm


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
    return render(request, "period_tracker.html", {'form': form})
