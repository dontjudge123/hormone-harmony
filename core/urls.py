from django.urls import path
from .views import period_tracker

app_name = 'core'

urlpatterns = [
    path('period/', period_tracker, name='period'),
]
from django.urls import path
from .views import period_tracker, symptom_tracker

urlpatterns = [
    path('period/', period_tracker, name='period_tracker'),
    path('cycle/<int:cycle_id>/symptoms/', symptom_tracker, name='symptom_tracker'),
]
