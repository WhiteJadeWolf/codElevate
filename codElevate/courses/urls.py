from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.index, name='index'),
    path('instructor/', views.instructor_dashboard, name='instructor_dashboard'),
    path('<int:course_id>/', views.course_detail, name='course_detail'),
    path('<int:course_id>/enroll/', views.enroll_course, name='enroll'),
    path('<int:course_id>/unenroll/', views.unenroll_course, name='unenroll'),
]