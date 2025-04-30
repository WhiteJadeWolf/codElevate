from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from .models import Course, Category
from login.models import UserType
from dashboard.models import CourseEnrollment, Progress
from .forms import CourseForm

def index(request):
    # Get user type if authenticated
    user_type = None
    if request.user.is_authenticated:
        try:
            user_type = UserType.objects.get(user=request.user).user_type
        except UserType.DoesNotExist:
            pass

    # Get filter parameters from request
    category = request.GET.get('category')
    level = request.GET.get('level')
    search = request.GET.get('search')
    sort = request.GET.get('sort', '-created_at')

    # Initialize the base queryset
    if user_type == 'instructor':
        # Instructors see only their own courses
        courses = Course.objects.filter(instructor=request.user)
    else:
        # Students and anonymous users see all courses
        courses = Course.objects.all()

    # Apply filters
    if category:
        courses = courses.filter(category__name=category)
    if level:
        courses = courses.filter(level=level)
    if search:
        courses = courses.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(instructor__username__icontains=search)
        )

    # Apply sorting
    if sort in ['title', '-title', 'created_at', '-created_at', 'duration', '-duration']:
        courses = courses.order_by(sort)

    # Get all categories for filter sidebar
    categories = Category.objects.all()
    levels = [choice[0] for choice in Course.LEVEL_CHOICES]

    context = {
        'courses': courses,
        'categories': categories,
        'levels': levels,
        'current_category': category,
        'current_level': level,
        'current_search': search,
        'current_sort': sort,
        'user_type': user_type
    }

    # Use different template for instructors
    if user_type == 'instructor':
        return render(request, 'courses/instructor_index.html', context)
    return render(request, 'courses/index.html', context)

@login_required
def create_course(request):
    # Check if user is an instructor
    try:
        user_type = UserType.objects.get(user=request.user)
        if user_type.user_type != 'instructor':
            raise PermissionDenied
    except UserType.DoesNotExist:
        raise PermissionDenied

    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            messages.success(request, 'Course created successfully!')
            return redirect('courses:course_detail', course_id=course.id)
    else:
        form = CourseForm()

    return render(request, 'courses/create_course.html', {'form': form})

@login_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    # Check if user is the course instructor
    if course.instructor != request.user:
        raise PermissionDenied
    
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully!')
            return redirect('courses:course_detail', course_id=course.id)
    else:
        form = CourseForm(instance=course)
    
    return render(request, 'courses/edit_course.html', {'form': form, 'course': course})

@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    # Check if user is the course instructor
    if course.instructor != request.user:
        raise PermissionDenied
    
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted successfully!')
        return redirect('courses:index')
    
    return render(request, 'courses/delete_course_confirm.html', {'course': course})

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    try:
        user_type = UserType.objects.get(user=request.user)
    except UserType.DoesNotExist:
        user_type = None
    
    # Check if user is enrolled
    is_enrolled = False
    if request.user.is_authenticated and user_type and user_type.user_type == 'student':
        is_enrolled = course.enrollments.filter(student=request.user).exists()

    context = {
        'course': course,
        'is_enrolled': is_enrolled,
        'user_type': user_type.user_type if user_type else None,
        'is_instructor': course.instructor == request.user,
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
        
        # Check if already enrolled
        if CourseEnrollment.objects.filter(student=request.user, course=course).exists():
            messages.warning(request, 'You are already enrolled in this course.')
            return redirect('courses:course_detail', course_id=course_id)
        
        # Create enrollment
        enrollment = CourseEnrollment.objects.create(
            student=request.user,
            course=course
        )
        # Create progress tracker
        Progress.objects.create(
            enrollment=enrollment,
            total_modules=0  # You can set this based on your course structure
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