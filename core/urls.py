from django.urls import path
from .views import period_tracker, symptom_tracker, cycle_dashboard

app_name = 'core'

urlpatterns = [
    path('period/', period_tracker, name='period'),
    path('cycle/<int:cycle_id>/symptoms/', symptom_tracker, name='symptom_tracker'),
    path('cycle/<int:cycle_id>/dashboard/', cycle_dashboard, name='cycle_dashboard'),
]
