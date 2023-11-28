
from django.contrib import admin
from django.urls import path, include
from  django.conf.urls.static import  static
from  django.conf import settings

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path('', include('technique.urls')),
    path('', include('commercial.urls')),
    path('', include('environnement.urls')),
    path('', include('authentication.urls')),
    path('', include('bunsess.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path("__debug__/", include("debug_toolbar.urls")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)