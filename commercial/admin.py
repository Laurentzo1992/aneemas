from django.contrib import admin
from .models import Client, DirectionLingot, EmplacementLingot, Factures, Fichecontrol, Lingot, MovementLingot, Pesee, FicheTarification, StragieTarification, TypeClient
from django.urls import path, reverse
from django.utils.html import format_html
from jet.admin import CompactInline

from django.contrib.admin import AdminSite
from django.urls import path, include
from technique import views

# Register your models here.
class LingotInLineAdmin(CompactInline):
    model = Lingot
    extra = 1
    show_change_link = True
    exclude = [
        'titre_carat',
        'ecart',
        'quantite_or_fin',
        'densite',
        'fiche_tarification'
    ]


class FichecontrolInlineAdmin(CompactInline):
    model = Fichecontrol
    extra = 1
    show_change_link = True
    exclude = [
        'titre_carat',
        'ecart',
        'quantite_or_fin',
        'densite',
        'fiche_tarification'
    ]

class PeseeInLineAdmin(CompactInline):
    model = Pesee
    extra = 1
    show_change_link = True
    exclude = [
        'titre_carat',
        'ecart',
        'quantite_or_fin',
        'densite',
        'fiche_tarification'
    ]

class FicheTarificationInlineAdmin(CompactInline):
    model = FicheTarification
    extra = 1
    show_change_link = True
    

class FichecontrolAdmin(admin.ModelAdmin):
    inlines = [LingotInLineAdmin, FicheTarificationInlineAdmin]
    list_display = ['numero', 'user', 'date_control', 'modified', 'custom_action_button']
    exclude = ['user']

    def custom_action_button(self, obj):
        generate_pdf_url = reverse('generate-fiche-control', args=[obj.pk])  # Replace 'generate_pdf' with your actual URL name
        return format_html('<a class="button printButton" data-url={}>Imprimer</a> <a class="button"\
        " default" href="#">Tarifier</a>', generate_pdf_url, generate_pdf_url)
    custom_action_button.allow_tags = True
    custom_action_button.short_description = 'Actions'  # Set a description for the column
    
    actions = ['tarifier']  # Add your custom action here

    def tarifier(self, request, queryset):
        # Perform your custom action here
        selected_ids = queryset.values_list('id', flat=True)
        # Do something with selected_ids

    tarifier.short_description = 'Tarifier'

class LingotAdmin(admin.ModelAdmin):
    inlines = [PeseeInLineAdmin]
    list_display = ['numero', 'fiche_control', 'date_reception', 'modified', 'custom_action_button']
    exclude = ['user']

    def custom_action_button(self, obj):
        return format_html('<a class="button" href="#">Tarification</a> <a class="button default" href="#">Control</a>')
    custom_action_button.allow_tags = True
    custom_action_button.short_description = 'Actions'  # Set a description for the column
    
    actions = ['tarifier']  # Add your custom action here

    def tarifier(self, request, queryset):
        selected_ids = queryset.values_list('id', flat=True)
        # Do something with selected_ids

    tarifier.short_description = 'Controller'

class ClientAdmin(admin.ModelAdmin):
    inlines = []
    list_display = ['nom', 'type_client']
    exclude = []

    def custom_action_button(self, obj):
        return format_html('<a class="button" href="#">Modifier</a> <a class="button default" href="#">Archiver</a>')
    custom_action_button.allow_tags = True
    custom_action_button.short_description = 'Actions'  # Set a description for the column
    
    actions = ['Archiver']  # Add your custom action here

    def tarifier(self, request, queryset):
        selected_ids = queryset.values_list('id', flat=True)

    tarifier.short_description = 'Archiver'

class CommercialAdmin(AdminSite):
    site_header = "Gestion commmercial"
    site_title = "Site gestion commercial"
    index_title = "Bievenue surGestion commmercial"

    name = "commercial_admin"
    label = "commercial_admin"
    site_name = "commercial_admin"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = []
    
        return urls + custom_urls


commercial_admin = CommercialAdmin(name="commercial_adminn")


admin.site.register(Fichecontrol, FichecontrolAdmin)


commercial_admin.register(Fichecontrol, FichecontrolAdmin)
commercial_admin.register(FicheTarification)
commercial_admin.register(Lingot, LingotAdmin)
commercial_admin.register(Factures)
commercial_admin.register(StragieTarification)
commercial_admin.register(Client, ClientAdmin)
commercial_admin.register(TypeClient)
commercial_admin.register(DirectionLingot)
commercial_admin.register(MovementLingot)
commercial_admin.register(EmplacementLingot)

