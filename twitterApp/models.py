from django.contrib.auth.models import User, UserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    objects = UserManager()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField(
        'self', related_name='followed_by', symmetrical=False, blank=True
    )

    def __str__(self):
        return self.user.username


class Tweet(models.Model):
    posted_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    tweet = models.CharField(max_length=255)
    likes_count = models.IntegerField(default=0)
    posted_date = models.DateTimeField('posted date', auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')

    def __str__(self):
        return self.tweet


class Comment(models.Model):
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    likes_count = models.IntegerField(default=0)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    comments = models.ManyToManyField('self', blank=True)
    posted_date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name='comment_likes')

    def __str__(self):
        return self.comment


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = UserProfile(user=instance)
        user_profile.save()
        user_profile.follows.set([instance.userprofile.id])
        user_profile.save()
