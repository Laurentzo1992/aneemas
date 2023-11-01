from django.contrib.admin import AdminSite
from django.urls import path, include
from technique import views

class CommercialAdmin(AdminSite):
    site_header = "Gestion commmercial"
    site_title = "Site gestion commercial"
    index_title = "Bievenue surGestion commmercial"

    name = "commercial_admin"
    label = "commercial_admin"
    site_name = "commercial_admin"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('enrolement/add', views.add, name='add_enrolement'),
            path('', include('technique.urls')),
            path('', include('commercial.urls')),
            path('', include('environnement.urls')),
            path('', include('authentication.urls')),
        ]
    
        return urls + custom_urls

commercial_admin = CommercialAdmin(name="commercial_admin")