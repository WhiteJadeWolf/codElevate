
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import CourseEnrollment, Progress
from assignments.models import Assignment, Submission
from login.models import UserType
from courses.models import Course
from myprofile.models import Profile

@login_required
def index(request):
    context = {}
    user = request.user
    user_type = None
    profile = None
    try:
        user_type_instance = UserType.objects.get(user=user)
        user_type = user_type_instance.user_type
    except UserType.DoesNotExist:
        pass
    except UserType.MultipleObjectsReturned:
         user_type_instance = UserType.objects.filter(user=user).first()
         user_type = user_type_instance.user_type if user_type_instance else None
         
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None
        
    context['user_type'] = user_type
    context['profile'] = profile

    if user_type == 'student':
        enrollments = CourseEnrollment.objects.filter(
            student=user
        ).select_related('course', 'progress')

        context['enrollments'] = enrollments

        total_courses = enrollments.count()
        completed_courses = enrollments.filter(completed=True).count()
        in_progress_courses = total_courses - completed_courses

        overall_progress_percentage = 0
        if total_courses > 0:
            total_progress_sum = 0
            valid_enrollments_for_avg = 0
            enrollments_with_progress = enrollments.filter(progress__isnull=False)
            if enrollments_with_progress.exists():
                for enr in enrollments_with_progress:
                    if enr.progress.total_modules > 0:
                        total_progress_sum += enr.progress.get_progress_percentage()
                        valid_enrollments_for_avg += 1
                if valid_enrollments_for_avg > 0:
                    overall_progress_percentage = int(total_progress_sum / valid_enrollments_for_avg)
                else:
                     overall_progress_percentage = int((completed_courses / total_courses) * 100) if total_courses > 0 else 0
            else:
                overall_progress_percentage = int((completed_courses / total_courses) * 100) if total_courses > 0 else 0

        context['total_courses'] = total_courses
        context['completed_courses'] = completed_courses
        context['in_progress_courses'] = in_progress_courses
        context['overall_progress_percentage'] = overall_progress_percentage

        now = timezone.now()
        enrolled_course_ids = list(enrollments.values_list('course_id', flat=True))
        upcoming_assignments_data = []
        if enrolled_course_ids:
            assignments = Assignment.objects.filter(
                course_id__in=enrolled_course_ids,
                due_date__gt=now
            ).select_related('course').order_by('due_date')
            
            submitted_assignment_ids = set(Submission.objects.filter(
                assignment__in=assignments,
                student=user,
                is_submitted=True
            ).values_list('assignment_id', flat=True))

            for assignment in assignments:
                is_submitted = assignment.id in submitted_assignment_ids
                upcoming_assignments_data.append({
                    'assignment': assignment,
                    'submission': {'is_submitted': is_submitted}
                })
        context['upcoming_assignments'] = upcoming_assignments_data

    elif user_type == 'instructor':
        instructor_courses = Course.objects.filter(instructor=user)
        context['instructor_courses'] = instructor_courses

    return render(request, 'dashboard/dashboard.html', context)