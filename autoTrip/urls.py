from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('trips.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('users/', include('users.urls')),
]
