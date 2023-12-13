from django.forms import Textarea
from commercial.admin import ClientAdmin, ControlAdmin, ControlBUMIGEBAdmin, ControlLingotAdmin, EmplacementLingotAdmin, FactureAdmin, FactureDefinitiveAdmin, FactureProformaAdmin, FicheTarificationAdmin,\
    FichecontrolAdmin, FonteAdmin, FournisseurAdmin, LingotAdmin,\
        LingotsDisponiblesPourVenteAdmin, ClientAdmin, SMS, MouvementLingotAdmin,\
        PayementAdmin, RapportAffiangeAdmin, SMSAdmin, SMSClientAdmin, SMSFournisseurAdmin, TransferedFicheTarificationAdmin, TransferedLingotAdmin, TypeSubstanceAdmin, VenteAdmin, VentesConcluAdmin
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

    def each_context(self, request):
        context = super().each_context(request)
        # Désactivez le lien "Voir le site" en définissant `site_url` à `None`
        context['site_url'] = None
        return context


    
    def get_urls(self):
        from django.urls import path
        urls = super(CommercialAdmin, self).get_urls()
        custom_urls = [
            # path('stock/fondre/<path:object_id>', self.admin_view(fondre_lingot), name="stock_fondre"),
            path('fonte/retour/', self.admin_view(fondre_lingot), name="fonte-retour"),
            path('commercial/paiment/<path:object_id>/transferer/', self.admin_view(commercial_tarification_transferer), name='commercial_tarification_transferer'),

            path('commercial/module-bi/', commercial_admin.admin_view(bi_view), name='module-bi'),
            path('commercial/bi-data/', commercial_admin.admin_view(bi_data), name='bi-data'),
            # path('stock/fondre/<path:object_id>', self.admin_view(fondre_lingot), name="stock_fondre"),
            path('fonte/retour/', commercial_admin.admin_view(fondre_lingot), name="fonte-retour"),
            path('commercial/paiment/<path:object_id>/transferer/', commercial_admin.admin_view(commercial_tarification_transferer), name='commercial_tarification_transferer'),
            path('commercial/fiche-control/<pk>/generate/', commercial_admin.admin_view(generate_fiche_control), name='generate-fichecontrol'),
            path('commercial/fiche-tarification/<pk>/generate/', commercial_admin.admin_view(generate_fiche_tarification), name='generate-fichetarification'),
            path('commercial/facture/<pk>/generate/', commercial_admin.admin_view(generate_facture), name='commercial_facture_generate'),
            path('commercial/facture/<pk>/view/', commercial_admin.admin_view(view_facture), name='commercial_facture_view'),
            path('commercial/payement/<pk>/generate/', commercial_admin.admin_view(generate_recu_payement_achat), name='generate_recu_payement_achat'),
            path('commercial/vente/lingots-disponible-pour-vente', commercial_admin.admin_view(lingots_disponibles_pour_vente_changelist), name="lingots_disponibles_pour_vente_changelist"),
        ]
        return custom_urls + urls

    # def my_view(self, request):
    #     return HttpResponse("Hello!")


commercial_admin = CommercialAdmin(name="gesco")

commercial_admin.register(Fichecontrol, FichecontrolAdmin)
commercial_admin.register(FicheTarification, FicheTarificationAdmin)
commercial_admin.register(Lingot, LingotAdmin)
commercial_admin.register(LingotsDisponiblesPourVente, LingotsDisponiblesPourVenteAdmin)
commercial_admin.register(TypeSubstance, TypeSubstanceAdmin)
commercial_admin.register(StragieTarification)
commercial_admin.register(Fournisseur, FournisseurAdmin)
commercial_admin.register(TypeFournisseur)
commercial_admin.register(DirectionLingot)
commercial_admin.register(MouvementLingot, MouvementLingotAdmin)
commercial_admin.register(EmplacementLingot, EmplacementLingotAdmin)
commercial_admin.register(ModePayement)
commercial_admin.register(Payement, PayementAdmin)
commercial_admin.register(Fonte, FonteAdmin)
commercial_admin.register(ControlBUMIGEB, ControlBUMIGEBAdmin)
commercial_admin.register(Vente, VenteAdmin)
commercial_admin.register(VentesConclu, VentesConcluAdmin)
commercial_admin.register(FactureProforma, FactureProformaAdmin)
commercial_admin.register(FactureDefinitive, FactureDefinitiveAdmin)
commercial_admin.register(RapportAffinage, RapportAffiangeAdmin)
commercial_admin.register(Client, ClientAdmin)
commercial_admin.register(RepresentantFournisseur)
commercial_admin.register(TypeDeClient)
commercial_admin.register(SMS, SMSAdmin)
commercial_admin.register(SMSFournisseur, SMSFournisseurAdmin)
commercial_admin.register(SMSClient, SMSClientAdmin)
commercial_admin.register(ControlLingot, ControlLingotAdmin)
commercial_admin.register(Control, ControlAdmin)
commercial_admin.register(Facture, FactureAdmin)

commercial_admin.register(TransferedFicheTarification, TransferedFicheTarificationAdmin)
commercial_admin.register(TransferedLingot, TransferedLingotAdmin)
commercial_admin.register(StructureDeControl)
commercial_admin.register(User)