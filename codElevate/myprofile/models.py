# myprofile/models.py
import os
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Helper function for upload path
def user_profile_picture_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/profile_pics/user_<id>/<filename>
    # Important: You might want to add logic to rename the file to avoid collisions
    # or use a UUID for the filename.
    _, extension = os.path.splitext(filename)
    new_filename = f"user_{instance.user.id}{extension}"
    return f'profile_pics/{new_filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to=user_profile_picture_path, null=True, blank=True, default='profile_pics/default.png') # Added default
    location = models.CharField(max_length=100, blank=True)
    # Add other fields as needed, e.g., website, birth_date

    def __str__(self):
        return f'{self.user.username} Profile'

    # Optional: Property to get picture URL, handling default
    @property
    def get_profile_picture_url(self):
        if self.profile_picture and hasattr(self.profile_picture, 'url'):
            return self.profile_picture.url
        else:
            # If using default='path/to/default.png' in ImageField, this might not be needed
            # depending on how you handle static/media. Explicitly returning static path is safer.
            from django.templatetags.static import static
            return static('images/default.png') # Assumes you have /static/images/default.png

# Signal to create or update user profile automatically when User is created/saved
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create a Profile for a new User, or ensure an existing User's Profile is saved
    (though saving on update is often not strictly necessary unless Profile fields
    depend on User fields that changed, which isn't the case here).
    """
    if created:
        # If the user was just created, create their profile.
        Profile.objects.create(user=instance)
        # No need to call instance.profile.save() here, create() already saved it.
    else:
        # If the user is being updated (like during login's last_login update),
        # ensure the profile exists before trying to save it.
        # This handles users created *before* the signal was implemented.
        try:
            instance.profile.save()
        except Profile.DoesNotExist:
            # If profile somehow doesn't exist for an existing user, create it.
            Profile.objects.create(user=instance)