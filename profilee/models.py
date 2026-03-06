from django.db import models
from django.contrib.auth.models import User

def user_directory_path(instance, filename):
    return f'userimg/{instance.user.id}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='profilee_profile'
    )
    phone = models.CharField(max_length=15, blank=True)
    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)

    def __str__(self):
        return self.user.username
