from django.urls import path
from knox.views import LogoutView

from users.views import RegisterView, LoginView, ProfileViewSet, ProfilesViewsSet

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('profile_list', ProfilesViewsSet.as_view, name='profile_list'),
    path('profile/<int:pk>', ProfileViewSet.as_view, name='profile')
]