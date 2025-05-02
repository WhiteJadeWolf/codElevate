from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Category
from login.models import UserType
from dashboard.models import CourseEnrollment, Progress
from assignments.models import Assignment, Submission
from django.db.models import Q

def index(request):
    category = request.GET.get('category')
    level = request.GET.get('level')
    search = request.GET.get('search')
    sort = request.GET.get('sort', '-created_at')

    courses = Course.objects.all()

    if category:
        courses = courses.filter(category__name=category)
    if level:
        courses = courses.filter(level=level)
    if search:
        search_filter = (
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(instructor__username__icontains=search)
        )
        courses = courses.filter(search_filter).distinct()

    if sort in ['title', '-title', 'created_at', '-created_at', 'duration', '-duration']:
        courses = courses.order_by(sort)
    else:
        courses = courses.order_by('-created_at')

    categories = Category.objects.all()
    levels = [choice[0] for choice in Course.LEVEL_CHOICES]

    context = {
        'courses': courses,
        'categories': categories,
        'levels': levels,
        'current_category': category,
        'current_level': level,
        'current_search': search,
        'current_sort': sort
    }

    if request.user.is_authenticated:
        try:
            user_type = UserType.objects.get(user=request.user)
            context['user_type'] = user_type.user_type
        except UserType.DoesNotExist:
            pass

    return render(request, 'courses/index.html', context)

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    is_enrolled = False
    enrollment = None
    assignments_with_status = []
    if request.user.is_authenticated:
        try:
            enrollment = CourseEnrollment.objects.select_related('progress').get(student=request.user, course=course)
            is_enrolled = True
        except:
            is_enrolled = False
            
        assignments = Assignment.objects.filter(course=course).order_by('due_date')
        submitted_assignment_ids = set(Submission.objects.filter(
            assignment__in=assignments,
            student=request.user,
            is_submitted=True
        ).values_list('assignment_id', flat=True))

        for assignment in assignments:
            assignments_with_status.append({
                'assignment': assignment,
                'is_submitted': assignment.id in submitted_assignment_ids
            })

    context = {
        'course': course,
        'is_enrolled': is_enrolled,
        'enrollment': enrollment,
        'course_assignments': assignments_with_status,
    }
    return render(request, 'courses/detail.html', context)

@login_required
def instructor_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login:index')
    
    try:
        user_type = UserType.objects.get(user=request.user)
        if user_type.user_type != 'instructor':
            return redirect('dashboard:index')
    except UserType.DoesNotExist:
        return redirect('dashboard:index')
    
    courses = Course.objects.filter(instructor=request.user)
    
    context = {
        'courses': courses,
    }
    
    return render(request, 'courses/instructor_dashboard.html', context)

@login_required
def enroll_course(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, id=course_id)
        
        if CourseEnrollment.objects.filter(student=request.user, course=course).exists():
            messages.warning(request, 'You are already enrolled in this course.')
            return redirect('courses:course_detail', course_id=course_id)
        
        enrollment = CourseEnrollment.objects.create(
            student=request.user,
            course=course
        )
        Progress.objects.create(
            enrollment=enrollment,
            total_modules=0
        )
        
        messages.success(request, f'Successfully enrolled in {course.title}')
        return redirect('courses:course_detail', course_id=course_id)
    return redirect('courses:index')

@login_required
def unenroll_course(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, id=course_id)
        enrollment = get_object_or_404(CourseEnrollment, student=request.user, course=course)
        
        enrollment.delete()
        messages.success(request, f'Successfully unenrolled from {course.title}')
        return redirect('courses:course_detail', course_id=course_id)
    return redirect('courses:index')