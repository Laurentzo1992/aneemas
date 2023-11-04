from django.contrib import admin
from .models import Client, DirectionLingot, EmplacementLingot, Factures, Fichecontrol, Fonte, Lingot, ModePayement, MouvementLingot, Pesee, FicheTarification, StragieTarification, TypeClient, TypeLingot
from django.urls import path, reverse
from django.utils.html import format_html
from jet.admin import CompactInline

from django.urls import path, include
from technique import views
from commercial import forms

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
        'fiche_tarification',
        'user'
    ]
    read_only_fields = ['user']

# Inline Pour les relation many to many
class FonteLingotInLineAdmin(CompactInline):
    model = Fonte.lingots.through
    extra = 1
    show_change_link = True
    exclude = [
        'titre_carat',
        'ecart',
        'quantite_or_fin',
        'densite',
        'fiche_tarification',
        'user'
    ]
    read_only_fields = ['user', 'lingot']

class LingotSimpleInLineAdmin(admin.TabularInline):
    model = Lingot

class FichecontrolInlineAdmin(CompactInline):
    model = Fichecontrol
    extra = 1
    show_change_link = True
    exclude = [
        'titre_carat',
        'ecart',
        'quantite_or_fin',
        'densite',
        'fiche_tarification',
        'user'
    ]
    readonly_fields = ['user']

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


class FonteAdmin(admin.ModelAdmin):
    inlines = [FonteLingotInLineAdmin]
    form = forms.FonteForm
    list_display = ['numero', 'date_fin', 'user', 'etat']
    exclude = ['user']
    show_change_link = True

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'lingots':
            # Limiter les lingot aux non associées
            kwargs['queryset'] = Lingot.objects.filter(fonte__isnull=True)
        return super().formfield_for_manytomany(db_field, request, **kwargs)
    

class FichecontrolAdmin(admin.ModelAdmin):
    inlines = [LingotInLineAdmin]
    list_display = ['numero', 'user', 'client', 'date_control', 'modified', 'custom_action_button']
    exclude = ['user']

    def custom_action_button(self, obj):
        generate_pdf_url = reverse('generate-fiche-control', args=[obj.pk])  # Replace 'generate_pdf' with your actual URL name
        return format_html('<a class="button print-button" href="#" data-url={}>Imprimer</a> <a class="button"\
        " default" href="{}">Tarifier</a>', generate_pdf_url, generate_pdf_url)
    custom_action_button.allow_tags = True
    custom_action_button.short_description = 'Actions'  # Set a description for the column
    
    actions = ['tarifier']  # Add your custom action here

    def tarifier(self, request, queryset):
        # Perform your custom action here
        selected_ids = queryset.values_list('id', flat=True)
        # Do something with selected_ids

    tarifier.short_description = 'Tarifier'

class FicheTarificationAdmin(admin.ModelAdmin):
    list_display = ['numero', 'user', 'client', 'date_tarification', 'modified', 'custom_action_button']
    exclude = ['user']

    def custom_action_button(self, obj):
        generate_pdf_url = reverse('generate-fiche-control', args=[obj.pk])  # Replace 'generate_pdf' with your actual URL name
        return format_html('<a class="button default print-button" href="#" data-url={}>Payer</a> <a class="button"\
        " href="#">Archiver</a>', generate_pdf_url, generate_pdf_url)
        
    custom_action_button.allow_tags = True
    custom_action_button.short_description = 'Actions'  # Set a description for the column
    
    actions = ['payer']  # Add your custom action here

    def tarifier(self, request, queryset):
        # Perform your custom action here
        selected_ids = queryset.values_list('id', flat=True)
        # Do something with selected_ids

    tarifier.short_description = 'Payer'

class LingotAdmin(admin.ModelAdmin):
    inlines = [PeseeInLineAdmin]
    list_display = ['numero', 'fiche_control', 'client', 'date_reception', 'modified', 'custom_action_button']
    exclude = ['user']
    readonly_fields = ['user']

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
    inlines = [FicheTarificationInlineAdmin, FichecontrolInlineAdmin, LingotInLineAdmin]
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

