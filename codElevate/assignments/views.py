from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import Http404

from courses.models import Course
from dashboard.models import CourseEnrollment
from .models import Assignment, Submission
from .forms import SubmissionForm

@login_required
def assignment_list(request):
    """
    Displays a list of assignments for courses the student is enrolled in.
    Separates upcoming/pending assignments from submitted/past due ones.
    """
    student = request.user

    enrolled_course_ids = CourseEnrollment.objects.filter(
        student=student
    ).values_list('course_id', flat=True)

    if not enrolled_course_ids:
        assignments = Assignment.objects.none()
    else:
        assignments = Assignment.objects.filter(
            course_id__in=enrolled_course_ids
        ).select_related('course').order_by('due_date')

    submissions_dict = {}
    for assignment in assignments:
        submission, created = Submission.objects.get_or_create(
            assignment=assignment,
            student=student,
        )
        submissions_dict[assignment.id] = submission

    now = timezone.now()
    upcoming_pending = []
    submitted_or_past = []
    total_assignments = assignments.count()

    for assignment in assignments:
        submission = submissions_dict[assignment.id]
        if submission.is_submitted or assignment.due_date < now:
            submitted_or_past.append({'assignment': assignment, 'submission': submission})
        else:
            upcoming_pending.append({'assignment': assignment, 'submission': submission})

    context = {
        'upcoming_pending': upcoming_pending,
        'submitted_or_past': submitted_or_past,
        'total_assignments': total_assignments,
        'upcoming_count': len(upcoming_pending),
    }
    return render(request, 'assignments/assignment_list.html', context)


@login_required
def assignment_detail(request, assignment_id):
    """
    Displays details for a specific assignment and handles file submission.
    """
    assignment = get_object_or_404(Assignment.objects.select_related('course', 'course__instructor'), id=assignment_id)
    student = request.user

    is_enrolled = CourseEnrollment.objects.filter(
        student=student,
        course=assignment.course
    ).exists()

    if not is_enrolled:
        raise Http404("You are not enrolled in the course for this assignment.")

    submission, created = Submission.objects.get_or_create(
        assignment=assignment,
        student=student
    )

    form = SubmissionForm(instance=submission)

    if request.method == 'POST':

        form = SubmissionForm(request.POST, request.FILES, instance=submission)
        if form.is_valid():
            updated_submission = form.save(commit=False)
            submission.hand_in(uploaded_file=updated_submission.file)
            messages.success(request, f"Successfully submitted assignment: {assignment.title}")
            return redirect('assignments:assignment_detail', assignment_id=assignment.id)
        else:
            messages.error(request, "There was an error with your submission. Please check the form.")

    context = {
        'assignment': assignment,
        'submission': submission,
        'form': form,
        'is_past_due': assignment.is_past_due,
        'can_submit': not submission.is_submitted
    }
    return render(request, 'assignments/assignment_detail.html', context)