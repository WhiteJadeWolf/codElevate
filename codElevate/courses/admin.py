from django.contrib import admin
from .models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'total_modules', 'created_at')
    list_filter = ('created_at', 'instructor')
    search_fields = ('title', 'description', 'instructor__username')
