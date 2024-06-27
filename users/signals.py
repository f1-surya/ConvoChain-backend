from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserProfile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = UserProfile(user=instance)
        user_profile.save()
        user_profile.follows.set([instance.userprofile.id])
        user_profile.save()
