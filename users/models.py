from django.contrib.auth.models import UserManager, User
from django.db import models


class UserProfile(models.Model):
    objects = UserManager()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField(
        'self', related_name='followed_by', symmetrical=False, blank=True
    )

    def __str__(self):
        return self.user.username
