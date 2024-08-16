from django.db.models import CharField, Model, OneToOneField, CASCADE

from meta.models import Meta


class Tweet(Model):
    meta = OneToOneField(Meta, on_delete=CASCADE)
    body = CharField(max_length=255)

    def __str__(self):
        return self.body
