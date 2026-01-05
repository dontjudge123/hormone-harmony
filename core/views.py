from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import PeriodCycleForm
from .models import PeriodCycle


@login_required
def period_tracker(request):
    if request.method == "POST":
        form = PeriodCycleForm(request.POST)
        if form.is_valid():
            cycle = form.save(commit=False)
            cycle.user = request.user
            cycle.save()
            return redirect("period_tracker")
    else:
        form = PeriodCycleForm()

    cycles = PeriodCycle.objects.filter(
        user=request.user
    ).order_by("-start_date")

    return render(
        request,
        "period_tracker.html",
        {
            "form": form,
            "cycles": cycles,
        }
    )

