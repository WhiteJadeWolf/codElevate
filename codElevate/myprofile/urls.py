from django.urls import path
from . import views

app_name = 'myprofile'

urlpatterns = [
    path('', views.profile_view, name='profile'),
    path('edit/', views.profile_edit, name='profile_edit'),
]