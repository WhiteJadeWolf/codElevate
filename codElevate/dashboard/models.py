from django.db import models
from django.contrib.auth.models import User
from courses.models import Course

class CourseEnrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    last_accessed = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['student', 'course']

    def __str__(self):
        return f"{self.student.username} - {self.course.title}"

class Progress(models.Model):
    enrollment = models.OneToOneField(CourseEnrollment, on_delete=models.CASCADE, related_name='progress')
    completed_modules = models.IntegerField(default=0)
    total_modules = models.IntegerField(default=0)
    
    def get_progress_percentage(self):
        if self.total_modules == 0:
            return 0
        return int((self.completed_modules / self.total_modules) * 100)

    def __str__(self):
        return f"{self.enrollment.student.username}'s progress in {self.enrollment.course.title}"
