from django.contrib import admin
from .models import CourseEnrollment, Progress

@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_at', 'completed', 'last_accessed')
    list_filter = ('completed', 'enrolled_at')
    search_fields = ('student__username', 'course__title')

@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'completed_modules', 'total_modules', 'get_progress_percentage')
    list_filter = ('completed_modules', 'total_modules')
    search_fields = ('enrollment__student__username', 'enrollment__course__title')
