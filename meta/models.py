from django.contrib.auth.models import User
from django.db.models import Model, ForeignKey, IntegerField, DateTimeField, ManyToManyField, CASCADE, CharField


class Meta(Model):
    author = ForeignKey(User, on_delete=CASCADE)
    likes_count = IntegerField(default=0)
    posted_date = DateTimeField('posted date', auto_now_add=True)
    likes = ManyToManyField(User, blank=True, related_name='likes')
    content_type = CharField(max_length=10)
