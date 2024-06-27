from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from meta.serializers import MetaSerializer
from .models import Comment


class CommentSerializer(ModelSerializer):
    meta = SerializerMethodField('get_meta')

    class Meta:
        model = Comment
        fields = '__all__'

    def get_meta(self, comment):
        meta = comment.meta
        serializer = MetaSerializer(instance=meta, context=self.context)
        return serializer.data
