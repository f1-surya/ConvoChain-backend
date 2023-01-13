from django.contrib.auth import login
from django.contrib.auth.models import User
from knox.views import LoginView as KnoxLoginView
from rest_framework.generics import CreateAPIView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from users.models import UserProfile
from users.serializers import RegisterSerializer, ProfileSerializer


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class LoginView(KnoxLoginView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)


class ProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()

    def get_serializer_class(self):
        return ProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.get(pk=self.request.pk)


class ProfilesViewsSet(ModelViewSet):
    def get_serializer_class(self):
        return ProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.exclude(self.request.user)
