from django.contrib import admin
from .models import Course, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'category', 'level', 'created_at')
    list_filter = ('level', 'category')
    search_fields = ('title', 'description', 'instructor__username')
    date_hierarchy = 'created_at'
    raw_id_fields = ('instructor',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'instructor', 'thumbnail')
        }),
        ('Classification', {
            'fields': ('category', 'level')
        }),
        ('Course Details', {
            'fields': ('duration',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
