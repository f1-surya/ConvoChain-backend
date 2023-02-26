from django.contrib import admin
from django.urls import path, include

from .views import GetData

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', GetData.as_view()),
    path('', include('tweets.urls')),
    path('', include('users.urls')),
    path('', include('comments.urls')),
    path('', include('retweets.urls'))
]

