from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    profile_image = models.ImageField(
        upload_to='profile_images/',
        null=True,
        blank=True,
        verbose_name='Profile Picture'
    )
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.username

    def get_profile_image_url(self):
        if self.profile_image:
            return self.profile_image.url
        return None