from commercial.admin import ControlBUMIGEBAdmin, FicheTarificationAdmin, FichecontrolAdmin, FonteAdmin, FournisseurAdmin, LingotAdmin, PayementAdmin, TransferedFicheTarificationAdmin
from .models import *
from django.contrib.admin import AdminSite

from .views import *

class CommercialAdmin(AdminSite):
    site_header = "Gestion commmercial SONASP"
    site_title = "Gestion commmercial SONASPcommercial"
    index_title = "Gestion commmercial SONASP"

    name = "gesco-admin"
    label = "gesco-admin"
    site_name = "gesco-admin"
    app_label = "commercial"
    label = "commercial"

    
    def get_urls(self):
        from django.urls import path
        urls = super(CommercialAdmin, self).get_urls()
        custom_urls = [
            path('paiement/', self.admin_view(paiement)),
            # path('stock/fondre/<path:object_id>', self.admin_view(fondre_lingot), name="stock_fondre"),
            path('fonte/retour/', self.admin_view(fondre_lingot), name="fonte-retour"),
        ]
        return custom_urls + urls

    # def my_view(self, request):
    #     return HttpResponse("Hello!")


commercial_admin = CommercialAdmin(name="gesco")

commercial_admin.register(Fichecontrol, FichecontrolAdmin)
commercial_admin.register(FicheTarification, FicheTarificationAdmin)
commercial_admin.register(Lingot, LingotAdmin)
commercial_admin.register(TypeSubstance)
commercial_admin.register(Factures)
commercial_admin.register(StragieTarification)
commercial_admin.register(Fournisseur, FournisseurAdmin)
commercial_admin.register(TypeFournisseur)
commercial_admin.register(DirectionLingot)
commercial_admin.register(MouvementLingot)
commercial_admin.register(EmplacementLingot)
commercial_admin.register(ModePayement)
commercial_admin.register(Payement, PayementAdmin)
commercial_admin.register(Fonte, FonteAdmin)   
commercial_admin.register(ControlBUMIGEB, ControlBUMIGEBAdmin)   

commercial_admin.register(TransferedFicheTarification, TransferedFicheTarificationAdmin)