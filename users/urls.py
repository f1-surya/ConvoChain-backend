from django.urls import path
from knox.views import LogoutView

from users.views import RegisterView, LoginView, ProfileView

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('profile/<str:username>/<str:query>', ProfileView.as_view(), name='profile'),
    path('profile', ProfileView.as_view(), name='put')
]
