from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    # Add more URL patterns for dashboard functionality as needed
]
