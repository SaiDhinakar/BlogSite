from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import  admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('Authenticate.urls')),
    path('home/', include('Home.urls')),
    path('settings/', include('Settings.urls')),
    path('', include('Home.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)