from django.db.models import Model, ForeignKey, CharField, CASCADE, OneToOneField

from meta.models import Meta


class Comment(Model):
    meta = OneToOneField(Meta, on_delete=CASCADE)
    parent = ForeignKey(Meta, on_delete=CASCADE, related_name='parent')
    body = CharField(max_length=255)

    def __str__(self):
        return self.body
