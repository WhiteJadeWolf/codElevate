# myprofile/urls.py
from django.urls import path
from . import views

app_name = 'myprofile'  # <-- Crucial for namespacing!

urlpatterns = [
    path('', views.profile_view, name='profile'),       # Renamed to 'profile' to match base.html
    path('edit/', views.profile_edit, name='profile_edit'),
]