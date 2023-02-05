from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.forms import EmailField

from rest_framework.fields import CharField, SerializerMethodField
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator

from users.models import UserProfile


class RegisterSerializer(ModelSerializer):
    first_name = CharField(required=True)
    last_name = CharField(required=True)
    email = EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = CharField(write_only=True, required=True, validators=[validate_password])

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

    class Meta:
        model = UserProfile
        exclude = ('follows',)

    def get_full_name(self, profile):
        return profile.user.first_name + ' ' + profile.user.last_name