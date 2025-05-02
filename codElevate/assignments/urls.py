from django.urls import path
from . import views

app_name = 'assignments'

urlpatterns = [
    path('', views.assignment_list, name='assignment_list'),
    path('<int:assignment_id>/', views.assignment_detail, name='assignment_detail'),
]