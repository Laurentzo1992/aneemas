from commercial.admin import *
from .models import *
from django.contrib.admin import AdminSite
from django.contrib import admin

class CommercialAdmin(AdminSite):
    site_header = "Gestion commmercial SONASP"
    site_title = "Gestion commmercial SONASPcommercial"
    index_title = "Gestion commmercial SONASP"

    name = "gesco-admin"
    label = "gesco-admin"
    site_name = "gesco-admin"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = []
    
        return urls + custom_urls


commercial_admin = CommercialAdmin(name="gesco")


admin.site.register(Fichecontrol, FichecontrolAdmin)


commercial_admin.register(Fichecontrol, FichecontrolAdmin)
commercial_admin.register(FicheTarification, FicheTarificationAdmin)
commercial_admin.register(Lingot, LingotAdmin)
commercial_admin.register(TypeLingot)
commercial_admin.register(Factures)
commercial_admin.register(StragieTarification)
commercial_admin.register(Client, ClientAdmin)
commercial_admin.register(TypeClient)
commercial_admin.register(DirectionLingot)
commercial_admin.register(MouvementLingot)
commercial_admin.register(EmplacementLingot)
commercial_admin.register(ModePayement)
commercial_admin.register(Fonte, FonteAdmin)