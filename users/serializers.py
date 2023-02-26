from django.contrib.auth.models import User
from rest_framework.fields import CharField, SerializerMethodField
from rest_framework.serializers import ModelSerializer

from users.models import UserProfile


class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class ProfileSerializer(ModelSerializer):
    user = CharField(source='user.username', read_only=True)
    full_name = SerializerMethodField('get_full_name')
    followed_by_user = SerializerMethodField('get_followed_by_user')

    class Meta:
        model = UserProfile
        exclude = ('follows',)

    def get_full_name(self, profile):
        return profile.user.first_name + ' ' + profile.user.last_name

    def get_followed_by_user(self, profile):
        requester_profile = UserProfile.objects.get(user=self.context['user'])
        return requester_profile.follows.filter(follows=profile).exists()
