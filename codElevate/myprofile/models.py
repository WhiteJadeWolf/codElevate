import os
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

def user_profile_picture_path(instance, filename):
    _, extension = os.path.splitext(filename)
    new_filename = f"user_{instance.user.id}{extension}"
    return f'profile_pics/{new_filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to=user_profile_picture_path, null=True, blank=True, default='profile_pics/default.png')
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    @property
    def get_profile_picture_url(self):
        if self.profile_picture and hasattr(self.profile_picture, 'url'):
            return self.profile_picture.url
        else:
            from django.templatetags.static import static
            return static('images/default.png')

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create a Profile for a new User, or ensure an existing User's Profile is saved
    (though saving on update is often not strictly necessary unless Profile fields
    depend on User fields that changed, which isn't the case here).
    """
    if created:
        Profile.objects.create(user=instance)
    else:
        try:
            instance.profile.save()
        except Profile.DoesNotExist:
            Profile.objects.create(user=instance)