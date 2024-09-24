from django.urls import path
from . import views

urlpatterns = [
    path('workouts/', views.workouts, name='workouts'),
    
]
