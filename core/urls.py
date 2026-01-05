from django.urls import path
from .views import period_tracker

urlpatterns = [
    path("period/", period_tracker),
]
