from django.contrib import admin
from django.urls import path, include

# Mettez à jour vos urlpatterns comme ceci :
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('tasks.urls')), 
]