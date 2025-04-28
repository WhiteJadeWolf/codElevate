# assignments/models.py
import os
from django.db import models
from django.contrib.auth.models import User
from courses.models import Course
from django.utils import timezone

# Helper function to define upload path per user/assignment
def submission_upload_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/assignments/submissions/user_<id>/assignment_<id>/<filename>
    return f'assignments/submissions/user_{instance.student.id}/assignment_{instance.assignment.id}/{filename}'

class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.course.title})"

    @property
    def is_past_due(self):
        return timezone.now() > self.due_date

    class Meta:
        ordering = ['due_date'] # Default order by due date

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignment_submissions')
    file = models.FileField(upload_to=submission_upload_path, blank=True, null=True)
    submitted_at = models.DateTimeField(null=True, blank=True) # Set when user clicks "Hand In"
    is_submitted = models.BooleanField(default=False)
    # Optional fields for grading later
    # grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    # feedback = models.TextField(blank=True, null=True)

    class Meta:
        # Ensure a student has only one submission record per assignment
        unique_together = ['assignment', 'student']
        ordering = ['-submitted_at', 'assignment__due_date']

    def __str__(self):
        status = "Submitted" if self.is_submitted else "Not Submitted"
        return f"Submission for '{self.assignment.title}' by {self.student.username} ({status})"

    def hand_in(self, uploaded_file=None):
        """Marks the assignment as submitted."""
        if uploaded_file:
            # Delete old file if exists and different
            if self.file and self.file.name != uploaded_file.name:
                 if os.path.isfile(self.file.path):
                     os.remove(self.file.path)
            self.file = uploaded_file
        self.is_submitted = True
        self.submitted_at = timezone.now()
        self.save()