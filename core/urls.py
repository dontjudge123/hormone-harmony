from django.urls import path
from .views import period_tracker

app_name = 'core'

urlpatterns = [
    path('period/', period_tracker, name='period'),
]
