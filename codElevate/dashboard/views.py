from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from login.models import UserType
from .models import CourseEnrollment, Progress

@login_required
def index(request):
    context = {
        'user_type': None,
        'enrollments': [],
        'total_courses': 0,
        'completed_courses': 0,
        'in_progress_courses': 0,
    }
    
    try:
        user_type = UserType.objects.get(user=request.user)
        context['user_type'] = user_type.user_type
        
        if user_type.user_type == 'student':
            enrollments = CourseEnrollment.objects.filter(student=request.user).select_related('course', 'progress')
            context['enrollments'] = enrollments
            context['total_courses'] = enrollments.count()
            context['completed_courses'] = enrollments.filter(completed=True).count()
            context['in_progress_courses'] = context['total_courses'] - context['completed_courses']
    except UserType.DoesNotExist:
        pass
    return render(request, 'dashboard/index.html', context)