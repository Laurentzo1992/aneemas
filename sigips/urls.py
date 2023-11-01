
from django.contrib import admin
from django.urls import path, include
from  django.conf.urls.static import  static
from  django.conf import settings

from sigips.admin import commercial_admin

urlpatterns = [
    path("admin/", admin.site.urls),
    path("commercial/", commercial_admin.urls),
    path('', include('technique.urls')),
    path('', include('commercial.urls')),
    path('', include('environnement.urls')),
    path('', include('authentication.urls')),
    path('api-auth/', include('rest_framework.urls'))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)