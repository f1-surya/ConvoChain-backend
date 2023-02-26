from django.db.models import Model, OneToOneField, CASCADE, ForeignKey

from meta.models import Meta


class ReTweet(Model):
    meta = OneToOneField(Meta, on_delete=CASCADE)
    content = ForeignKey(Meta, on_delete=CASCADE, related_name='refers')

    def __str__(self):
        return self.content.tweet.body
