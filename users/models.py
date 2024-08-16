from django.contrib.auth.models import UserManager, User
from django.db.models import OneToOneField, ManyToManyField, Model, CASCADE, IntegerField, CharField


class UserProfile(Model):
    objects = UserManager()
    user = OneToOneField(User, on_delete=CASCADE)
    follows = ManyToManyField(
        'self', related_name='followed_by', symmetrical=False, blank=True
    )
    following_count = IntegerField(default=0)
    followers_count = IntegerField(default=0)
    about = CharField(max_length=160, blank=True, default='')

    def __str__(self):
        return self.user.username
