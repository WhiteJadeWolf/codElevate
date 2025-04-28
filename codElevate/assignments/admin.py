# assignments/admin.py
from django.contrib import admin
from .models import Assignment, Submission

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'due_date', 'created_at')
    list_filter = ('course', 'due_date')
    search_fields = ('title', 'description', 'course__title')
    date_hierarchy = 'due_date'

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'is_submitted', 'submitted_at', 'file_link')
    list_filter = ('is_submitted', 'assignment__course', 'assignment__due_date', 'submitted_at')
    search_fields = ('student__username', 'student__email', 'assignment__title')
    readonly_fields = ('submitted_at',) # Make submitted_at read-only in admin
    list_select_related = ('assignment', 'student', 'assignment__course') # Optimize queries

    def file_link(self, obj):
        from django.utils.html import format_html
        if obj.file:
            return format_html('<a href="{}" target="_blank">View File</a>', obj.file.url)
        return "No file"
    file_link.short_description = 'File'
    file_link.allow_tags = True # Necessary for older Django versions