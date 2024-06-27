from django.contrib import admin
from django.urls import path, include

from .views import GetData

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/', GetData.as_view()),
    path('api/', include('tweets.urls')),
    path('api/', include('users.urls')),
    path('api/', include('comments.urls')),
    path('api/', include('retweets.urls'))
]
