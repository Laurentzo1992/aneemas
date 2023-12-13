from decimal import Decimal
from typing import Any
from django.contrib import admin
from django.forms import BaseInlineFormSet, CharField, DecimalField, Textarea, ValidationError
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.db import IntegrityError, models, transaction
from django.http.request import HttpRequest
from django.shortcuts import render
from werkzeug import Client

from authentication.models import User
from commercial.module_sms import envoyer_message
from commercial.querysets import stock_queryset
from commercial.views import commercial_payement_archiver_view, commercial_tarification_transferer
from .models import (
    SMS,
    TYPE_CONTROL,
    TYPES_FACTURE,
    Control,
    ControlBUMIGEB,
    ControlLingot,
    Facture,
    FactureDefinitive,
    FactureProforma,
    Fichecontrol,
    Fournisseur,
    DirectionLingot,
    EmplacementLingot,
    FicheTarification,
    Fonte, Lingot,
    LingotFondus,
    ModePayement,
    MouvementLingot,
    MouvementLingotLingot,
    Payement,
    Pesee,
    FicheTarification,
    PieceJointe,
    PourcentageSubstanceControlBUMIGEB,
    PourcentageSubstanceControlLingot,
    PourcentageSubstanceLingot,
    PourcentageSubstanceRapportAffinage,
    PrixDesSubstances,
    RapportAffinage,
    StragieTarification,
    TransferedFicheTarification,
    TransferedFicheTarificationManager,
    TypeFournisseur,
    TypeSubstance,
    Vente,
    Client
    )
from django.urls import path, reverse, resolve
from django.utils.html import format_html
from jet.admin import CompactInline

from django.urls import path, include
from technique import views
from commercial import forms
from django.contrib import messages
from django.utils import timezone

from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator
from django.contrib.humanize.templatetags.humanize import intcomma
from django.utils.translation import gettext as _
from django.db.models import Q
from django.shortcuts import redirect
from django.contrib import admin, messages

from django.template.defaultfilters import escape


class PeseeInLineAdmin(CompactInline):
    model = Pesee
    formset = forms.PeseeInlineFormset
    extra = 1
    min_num = 1
    show_change_link = True
    exclude = [
        'titre_carat',
        'ecart',
        'quantite_or_fin',
        'densite',
        'fiche_tarification'
    ]
    readonly_fields = [
        'date_pesee'
    ]

    fields = [
        'poids_brut',
        'poids_immerge',
        'observation',
        ('actif', 'date_pesee')
    ]
    verbose_name = "Neauveau"
    verbose_name_plural = "Pesees"


class LingotInLineAdmin(CompactInline):
    model = Lingot
    extra = 0
    show_change_link = True
    inlines = [PeseeInLineAdmin]
    fields = [
        'poids_brut',
        'poids_immerge',
        'titre',
        'ecart',
        'densite',
        'or_fin',
        'observation',
    ]

    readonly_fields = [
        'poids_brut',
        'poids_immerge',
        'titre',
        'ecart',
        'densite',
        'or_fin'
    ]

class LingotTabularInLineAdmin(admin.TabularInline):
    model = Lingot
    extra = 1
    max_num = 100
    show_change_link = True
    inlines = [PeseeInLineAdmin]
    fields = [
        'poids_brut',
        'poids_immerge',
        'titre',
        'ecart',
        'densite',
        'or_fin',
        'observation',
    ]

    readonly_fields = [
        'poids_brut',
        'poids_immerge',
        'titre',
        'ecart',
        'densite',
        'or_fin'
    ]

class LingotBumigebInlineAdmin(admin.TabularInline):
    model = Lingot
    extra = 0
    show_change_link = True
    fields = [
        'numero',
        'numero_bumigeb',
        'poids_brut_bumigeb',
        'poids_immerge_bumigeb',
        'titre_bumigeb',
        'or_fin_bumigeb',
        'observation_bumigeb',
    ]
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3})},
    }

    readonly_fields = [
        'numero',
        'numero_bumigeb',
        'poids_brut',
        'poids_immerge',
        'titre',
        'ecart',
        'densite',
        'or_fin'
    ]

    def has_delete_permission(self, request, obj=None):
        return False  # Disable the ability to delete items

    def has_add_permission(self, request, obj=None):
        return False  # Disable the ability to delete items

class LingotBumigebInlineAdminReadOnly(admin.TabularInline):
    model = Lingot
    extra = 0
    show_change_link = True
    fields = [
        'numero',
        'numero_bumigeb',
        'poids_brut_bumigeb',
        'poids_immerge_bumigeb',
        'titre_bumigeb',
        'or_fin_bumigeb',
        'observation_bumigeb',
    ]
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3})},
    }

    readonly_fields = [
        'numero',
        'poids_brut',
        'poids_immerge',
        'titre',
        'ecart',
        'densite',
        'or_fin'
    ]

    def get_readonly_fields(self, request, obj=None):
        # all_fields = [field.name for field in self.model._meta.get_fields()]
        if 'rt' in request.GET:
            return self.readonly_fields
        else:
            return self.readonly_fields + ['numero_bumigeb']



    def has_delete_permission(self, request, obj=None):
        return False  # Disable the ability to delete items

    def has_add_permission(self, request, obj=None):
        return False  # Disable the ability to delete items


# Inline Pour les relation many to many
class FonteLingotInLineAdmin(admin.TabularInline):
    model = LingotFondus
    extra = 1
    max_num = 1
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

class LingotFonduInlineAdmin(admin.TabularInline):
    model = LingotFondus
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
    inlines = [LingotInLineAdmin]

class FichecontrolLingotInlineAdmin(admin.TabularInline):
    model = Lingot
    inlines = []
    extra = 0
    show_change_link = True
    verbose_name_plural = "Lingots Associes"
    verbose_name = "Lingot"


    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class LingotSimpleInLineAdmin(admin.TabularInline):
    model = Lingot

class FichecontrolInlineAdmin(CompactInline):
    model = FicheTarification
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


class FicheTarificationInlineAdmin(CompactInline):
    model = FicheTarification
    extra = 1
    show_change_link = True



class PourcentageSubstanceLingotInline(admin.TabularInline):
    model = PourcentageSubstanceLingot
    extra = 0
    formset =  forms.PourcentageSubstanceLingotFormset

class PourcentageSubstanceControlLingotInline(admin.TabularInline):
    model = PourcentageSubstanceControlLingot
    extra = 0
    show_change_link = True
    formset =  forms.PourcentageSubstanceControlLingotFormset


class ControlLingotInline(admin.TabularInline):
    model = ControlLingot
    extra = 0

class ControlLingotInline(admin.TabularInline):
    model = ControlLingot
    extra = 0
    show_change_link = True
    exclude = ['type', 'user', 'type_de_control']
    readonly_fields = ['numero', 'lingot', 'control']
    fields = [
                'lingot', 'numero_lingot_control',
                'poids_brut',  'poids_immerge', 'ecart',
                'or_fin', 'densite', 'titre_carat',
                'observation'
            ]

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 1})},
    }

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj):
        return False

class ControInlineAdmin(CompactInline):
    model=Control
    show_change_link = True
    extra = 0
    exclude = ['user']
    readonly_fields = ['numero_de_control']
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 1})},
    }


    def has_add_permission(self, request, obj):
        return False


class PourcentageSubstanceControlBUMIGEBFormset(BaseInlineFormSet):
    def clean(self):
        cleaned_data = super().clean()
        total_pourcentage = 0
        reste_count = 0
        total_reste_percentage = 0

        for form in self.forms:
            if not form.cleaned_data.get('DELETE'):
                pourcentage = form.cleaned_data.get('pourcentage') or 0

                if not form.cleaned_data.get('DELETE') and form.cleaned_data.get('reste'):
                    reste_count += 1
                else:
                    total_pourcentage += pourcentage

        if reste_count > 1:
            raise forms.ValidationError('Vous ne pouvez pas désigner plusieurs substance comme reste.')

        reste_percentage = 0
        if reste_count == 1:
            # Calculate the percentage for the metal with reste=True
            reste_percentage = 100 - total_pourcentage
            if reste_percentage < 0:
                raise forms.ValidationError('Le total des pourcentages doit être égal à (100).')

            # Set the calculated percentage in the form
            for form in self.forms:
                if not form.cleaned_data.get('DELETE') and form.cleaned_data.get('reste'):
                    form.cleaned_data['pourcentage'] = reste_percentage
                    return cleaned_data
        if total_pourcentage + reste_percentage != 100:
            raise forms.ValidationError('Le total des pourcentages doit être égal à 100.')

        return cleaned_data

    def save(self, commit=True):
        super().save(commit=False)
        instances = PourcentageSubstanceControlBUMIGEB.objects.filter(control_bumigeb=self.instance)
        # Set the auto computed pourcentage for the reste substance
        # Setting it in the clean() does not persit it the db
        for form, instance in zip(self.forms, instances):
            # Perform any modifications to the instance before saving
            if form.cleaned_data.get('reste'):
                instance.pourcentage = form.cleaned_data['pourcentage']
                if commit:
                    instance.save()

        return super().save(commit=commit)


class PourcentageSubstanceControlBUMIGEBInline(admin.TabularInline):
    model = PourcentageSubstanceControlBUMIGEB
    extra = 0
    formset =  PourcentageSubstanceControlBUMIGEBFormset


class PourcentageSubstanceRapportAffinageFormset(BaseInlineFormSet):
    def clean(self):
        cleaned_data = super().clean()
        total_pourcentage = 0
        reste_count = 0
        total_reste_percentage = 0

        for form in self.forms:
            if not form.cleaned_data.get('DELETE'):
                pourcentage = form.cleaned_data.get('pourcentage') or 0

                if not form.cleaned_data.get('DELETE') and form.cleaned_data.get('reste'):
                    reste_count += 1
                else:
                    total_pourcentage += pourcentage

        if reste_count > 1:
            raise forms.ValidationError('Vous ne pouvez pas désigner plusieurs substance comme reste.')

        reste_percentage = 0
        if reste_count == 1:
            # Calculate the percentage for the metal with reste=True
            reste_percentage = 100 - total_pourcentage
            if reste_percentage < 0:
                raise forms.ValidationError('Le total des pourcentages doit être égal à (100).')

            # Set the calculated percentage in the form
            for form in self.forms:
                if not form.cleaned_data.get('DELETE') and form.cleaned_data.get('reste'):
                    form.cleaned_data['pourcentage'] = reste_percentage
                    return cleaned_data
        if total_pourcentage + reste_percentage != 100:
            raise forms.ValidationError('Le total des pourcentages doit être égal à 100.')

        return cleaned_data

    def save(self, commit=True):
        super().save(commit=False)
        instances = PourcentageSubstanceRapportAffinage.objects.filter(rapport_affinage=self.instance)
        # Set the auto computed pourcentage for the reste substance
        # Setting it in the clean() does not persit it the db
        for form, instance in zip(self.forms, instances):
            # Perform any modifications to the instance before saving
            if form.cleaned_data.get('reste'):
                instance.pourcentage = form.cleaned_data['pourcentage']
                if commit:
                    instance.save()

        return super().save(commit=commit)


class PourcentageSubstanceRapportAffinageInline(admin.TabularInline):
    model = PourcentageSubstanceRapportAffinage
    extra = 0
    formset =  PourcentageSubstanceRapportAffinageFormset

class PrixSubstanceInlineAdmin(admin.TabularInline):
    model = PrixDesSubstances
    extra = 0
    exclude = ['user', 'control_lingot']
    readonly_fields = ['poids', 'prix']
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 1})},
    }
    fields = ['type_de_substance', 'poids', 'cours_de_substance', 'reduction_commercial', 'prix', 'observation']

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj):
        return False


class FactureProformaInlineAdmin(admin.StackedInline):
    model = FactureProforma
    formset = forms.FactureInlineFormSet
    extra = 0
    max_num = 1
    exclude = ['type_de_facture', 'archived', 'user']
    show_change_link = True
    readonly_fields = ['numero']
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 1})},
    }


    def get_readonly_fields(self, request, obj=None):
        # Check if a specific parameter is present in the request
        # print('get_readonly_fields:::obj', obj)
        facture_proformas = FactureProforma.objects.filter(vente=obj)
        if len(facture_proformas) > 0:
            return ['numero']

        # Default to the original readonly_fields
        return super().get_readonly_fields(request, obj)


class RapportAffinageInlineAdmin(admin.StackedInline):
    model = RapportAffinage
    formset = forms.ControlInlineFormSet
    extra = 0
    max_num = 1
    show_change_link = True
    exclude = ['user', 'type_de_control']
    readonly_fields = ['numero_de_control']
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 1})},
    }


class FactureDefinitiveInlineAdmin(admin.StackedInline):
    model = FactureDefinitive
    # formset = forms.FactureDefitiveInlineFormSet
    extra = 0
    max_num = 1
    exclude = ['type_de_facture',  'archived', 'user']
    show_change_link = True
    readonly_fields = ['numero']
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 1})},
    }

class NumeroFilter(admin.SimpleListFilter):
    title = 'Numero'
    parameter_name = 'numero'
    def __init__(self, request, params, model, model_admin):
        super().__init__(request, params, model, model_admin)
        lookup_choices = [('a', 'b')]
    def lookups(self, request, model_admin):
        # Retrieve distinct values for the virtual property 'numero'
        distinct_numeros = Fonte.objects.distinct()
        fontes = Fonte.objects.distinct()
        # Generate lookup options as (id, numero) pairs
        return [(item.id, item.numero) for item in fontes]

    def queryset(self, request, queryset):
        self.local_queryset = self.queryset
        def mlookups(self, request, model_admin):

            return [(item.id, item.numero) for item in  self.local_queryset]
        # Filter the queryset based on the selected 'numero'
        self.lookups = mlookups
        value = self.value()
        if value:
            return queryset.filter(id=value)
        return queryset

class IsMeltedFilter(admin.SimpleListFilter):
    title = 'Est fondu'
    parameter_name = 'is_melted'

    def lookups(self, request, model_admin):
        return [
            (None, 'Non'),
            ('yes', 'Oui'),
            ('no', 'Non'),
        ]

    def choices(self, cl):
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == lookup,
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(fonte__isnull=False)
        elif self.value() == 'no' or self.value() == None:
            return queryset.filter(fonte__isnull=True)
        return queryset

class LingotControlBUMIGEBFilter(admin.SimpleListFilter):
    title = _('No. lot BUMIGEB')
    parameter_name = 'control_bumgeb'

    def lookups(self, request, model_admin):
        # Retrieve distinct ControlBUMIGEB instances related to lingot
        control_bumigeb_instances = ControlBUMIGEB.objects.values_list('id', 'numero_lot').distinct()
        return control_bumigeb_instances

    def queryset(self, request, queryset):
        # Filter Lingots instances based on the selected ModelB
        contol_bumigeb_id = self.value()
        if contol_bumigeb_id:
            return queryset.filter(control_bumigeb__id=contol_bumigeb_id)
        return queryset

class FonteAdmin(admin.ModelAdmin):
    inlines = [FonteLingotInLineAdmin]
    form = forms.FonteAdminForm
    list_display = ['numero', 'resultant_lingot', 'date_sortie', 'date_retour', 'user', 'etat', 'custom_actions']
    exclude = ['user', 'date_retour', 'date_sortie', 'etat', 'fondu', 'archived']
    list_filter = [NumeroFilter]
    show_change_link = True

    # capture the request object to retrieve the GET parameters
    is_etat_in_filter = None
    request = None
    def changelist_view(self, request, extra_context=None):
        self.request = request
        self.is_etat_in_filter = request.GET.get('etat__exact') == 'in'
        return super().changelist_view(request, extra_context=extra_context)


    def get_filters_params(self, request, *args, **kwargs):
        params = super().get_filters_params(request, *args, **kwargs)

        # Set a default value for the custom filter if it's not present in the request
        if 'etat__exact' not in params:
            params['etat__exact'] = 'out'
        return params

    def get_list_display(self, request):
        # Check if a specific parameter is present in the request
        status = request.GET.get('etat__exact')
        default_list_display =   ['numero', 'resultant_lingot', 'date_sortie', 'date_retour', 'valider_par', 'etat', 'custom_actions']
        # If the parameter is present, modify the list_display accordingly
        if status:
            if status == 'out':
                list_display = ['numero', 'date_sortie', 'user', 'etat', 'custom_actions']
                return list_display
            elif status == 'in':
                list_display = ['numero', 'resultant_lingot', 'date_sortie', 'date_retour', 'valider_par', 'etat', 'custom_actions']
                return list_display

        # Return the default list_display if no specific parameter is present
        return default_list_display

    def resultant_lingot(self, obj):
        # Your custom logic to generate the value for the custom field
        url = reverse('gesco:commercial_lingot_change', args=[14])
        if obj.etat == 'in':
            lingot_fondus = LingotFondus.objects.get(fonte=obj)
            url = reverse('gesco:commercial_lingot_change', args=[lingot_fondus.lingot.pk])
            return format_html('<a href="{}">{}</a>', url, lingot_fondus.lingot)

    resultant_lingot.short_description = "Lingot resultant"
    short_description = 'Fonte'

    def save_model(self, request, obj, form, change):
        # Save the Payment model
        if not form.is_valid():
            self.message_user(request, "L'operation a echouée. Erreur interne!")
            return

        if not change and not obj.user:  # Check if the object is being created (not updated)
            obj.user = request.user
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form

        # if obj is None:
            # return forms.SortieFonteAdminForm
        # else:
            # return forms.RetourFonteAdminForm
            # form.base_fields['lingots'].queryset = Lingot.objects.filter(fonte__isnull=True) | obj.lingots.all()
            # form.base_fields['poids_brut'] = CharField(label='Additional Field', required=False)
        # return form

    # def change_view(self, request, object_id, form_url='', extra_context=None):
    #     # Override the change view to add your virtual fields
    #     extra_context = extra_context or {}

    #     # Fetch the instance of the model
    #     obj = self.get_object(request, object_id)

    #     # Create a form instance with the virtual fields
    #     form = forms.RetourFonteAdminForm(instance=obj)

    #     # Add the form instance to the extra context
    #     extra_context['adminform'] = form

    #     # Proceed with the default change view
    #     return super().change_view(request, object_id, form_url=form_url, extra_context=extra_context)

    def custom_actions(self, obj):
        class_name = 'disabled-link' if self.is_etat_in_filter else ''
        fondre_url = reverse('gesco:commercial_lingot_add')
        return format_html('<a class="button default {}" href="{}?ft={}">Valider</a>', class_name, fondre_url, obj.id)

    custom_actions.short_description = "Actions"

    # def formfield_for_manytomany(self, db_field, request, **kwargs):
    #     if db_field.name == 'lingots' and request.method == 'GET':
    #         # Set initial data for the many-to-many field
    #         instance = kwargs.get('instance')
    #         if instance:
    #             kwargs['initial'] = instance.lingots.all()

        # return super().formfield_for_manytomany(db_field, request, **kwargs)


class ControlBUMIGEBAdmin(admin.ModelAdmin):
    model = ControlBUMIGEB
    form = forms.ControlBUMIGEBAdminForm
    inlines = [LingotBumigebInlineAdminReadOnly, PourcentageSubstanceControlBUMIGEBInline]
    list_display = ['numero_lot', 'date_sortie', 'date_retour', 'user', 'etat', 'custom_actions']
    exclude = ['user', 'date_retour', 'etat', 'archived', 'reintegrer_par']
    # list_filter = [NumeroFilter]
    show_change_link = True


    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3})},
    }

    is_etat_in_filter = None
    request = None
    # capture the request object to retrieve the GET parameters

    def changelist_view(self, request, extra_context=None):
        self.request = request
        self.is_etat_in_filter = request.GET.get('etat__exact') == 'in'

        return super(ControlBUMIGEBAdmin, self).changelist_view(request, extra_context=None)

    def response_change(self, request, obj):
        if 'rt' in request.GET and obj.etat == 'in':
            return HttpResponseRedirect(reverse('gesco:commercial_controlbumigeb_changelist') + '?etat__exact=in')
        return super().response_change(request, obj)

    def custom_actions(self, obj):
        class_name = 'disabled-link' if self.is_etat_in_filter else ''
        fondre_url = reverse('gesco:commercial_controlbumigeb_change', args=[obj.id])
        return format_html('<a class="button default {}" href="{}?rt={}">Reintegrer</a>', class_name, fondre_url, obj.id)

    def save_model(self, request, obj, form, change):
        # Save the model
        super().save_model(request, obj, form, change)

        if not change and not obj.user:  # Check if the object is being created (not updated)
            obj.reintegrer_par = request.user

        fichecontrol_id = request.GET.get('a')
        # Check if the related object exists
        if 'rt' in request.GET:
            try:
                obj.etat = 'in'
                obj.date_retour = timezone.now()
            except TransferedFicheTarification.DoesNotExist:
                raise Http404(f"La fiche de control correspondante n'existe pas!")

        super().save_model(request, obj, form, change)

class TarifiedFilter(admin.SimpleListFilter):
    title = _('Tarifié')
    parameter_name = 'tarified'

    def lookups(self, request, model_admin):
        return (
            ('yes', _('Oui')),
            ('no', _('Non')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(fichetarification__isnull=False)
        elif self.value() == 'no':
            return queryset.filter(fichetarification__isnull=True)

class FichecontrolAdmin(admin.ModelAdmin):
    form = forms.FicheControlAdminForm
    inlines = [LingotInLineAdmin]
    # inlines = [LingotTabularInLineAdmin]
    list_display = ['numero', 'user_link', 'fichetarification_link', 'fournisseur', 'date_control', 'modified', 'custom_action_button']
    exclude = ['user', 'archived']
    readonly_fields = ['numero']
    list_filter = ['numero', 'user', 'fournisseur', 'lingot', TarifiedFilter]

    def custom_action_button(self, obj):
        generate_pdf_url = reverse('gesco:generate-fichecontrol', args=[obj.pk])  # Replace 'generate_pdf' with your actual URL name
        url_tarifier = reverse('gesco:commercial_fichetarification_add')
        return format_html(
            '<a class="button default" href="{}?a={}">Tarifier</a>'
            '<a class="button print-button" href="#" data-url={}>Imprimer</a>',
            url_tarifier, obj.id,
            generate_pdf_url,
            generate_pdf_url
        )
    custom_action_button.allow_tags = True
    custom_action_button.short_description = 'Actions'  # Set a description for the column

    actions = ['tarifier']  # Add your custom action here

    # def tarifier(self, request, queryset):
    #     # Perform your custom action here
    #     selected_ids = queryset.values_list('id', flat=True)
    #     # Do something with selected_ids


    def user_link(self, obj):
        if obj.user:
            return format_html('<a href="%s">%s</a>' % (reverse("gesco:authentication_user_change", args=(obj.user.pk,)), escape(obj.user)))
        else:
            return None

    user_link.allow_tags = True
    user_link.short_description = "Utilisateur"

    def fichetarification_link(self, obj):
        fichetarification = obj.fichetarification
        if not fichetarification is None:
            return format_html('<a href="%s">%s</a>' % (reverse("gesco:commercial_fichetarification_change", args=(fichetarification.pk,)), escape(fichetarification)))
        else:
            return None

    fichetarification_link.allow_tags = True
    fichetarification_link.short_description = "Fiche de tarification"

    def response_change(self, request, obj):
        # Your existing response_change logic here

        post_url_continue = request.POST.get("_continue", None)
        post_url_addanother = request.POST.get("_addanother", None)

        if not (post_url_continue or post_url_addanother):
            # The user didn't click "Save and continue editing" or "Save and add another"
            # Redirect to a different URL after saving changes
            obj_url = reverse('gesco:commercial_fichecontrol_change', args=[obj.pk])
            message = format_html('La fiche control « <a href="{}">{}</a> » a été modifié avec succès.', obj_url, obj)
            self.message_user(request, message, level=messages.SUCCESS)
            url = reverse('gesco:commercial_fichecontrol_changelist') + '?ft__isnull=1'
            return HttpResponseRedirect(url)

        return super().response_change(request, obj)
        
    def response_add(self, request, obj, post_url_continue=None):
        # Check if the 'your_variable' is present in the request
        if 'a' in request.GET and request.method == 'POST' and "_save" in request.POST:
            # If the variable is present, customize the redirect URL
            obj_url = reverse('gesco:commercial_fichecontrol_change', args=[obj.pk])
            message = format_html('La fiche control « <a href="{}">{}</a> » a été ajouté avec succès.', obj_url, obj)
            self.message_user(request, message, level=messages.SUCCESS)
            return HttpResponseRedirect(reverse('gesco:commercial_fichecontrol_changelist') + '?ft__isnull=1')

        # If the variable is not present, use the default redirect URL
        return super().response_add(request, obj, post_url_continue)
    
    def get_queryset(self, request):
        # Get the original queryset
        queryset = super().get_queryset(request)
        return queryset
        fichecontrol_associated = FicheTarification.objects.all().values_list('fichecontrol_id', flat=True)

        # Exclude instances associated
        queryset = queryset.exclude(id__in=fichecontrol_associated)
        return queryset

    def tarifier(self, request, queryset):
        for fichecontrol in queryset:
            # Check if a related ModelB instance exists
            if not fichecontrol.fichetarification_set.exists():
                # If not, create a new ModelB instance
                fichetarification = FicheTarification(fichecontrol=fichecontrol, user=request.user)
                fichetarification.created = fichetarification.modified = timezone.now()
                fichetarification.save(request)
                year = fichetarification.created.year
                self.message_user(request, f'Fiche de Tarification creé pour {fichecontrol}')
            else:
                fichetarification = FicheTarification.objects.get(fichecontrol=fichecontrol)
                self.message_user(request, f'La fiche de control {fichecontrol} est deja associé a une tarification {fichetarification.numero}', messages.WARNING)

    tarifier.short_description = "Tarifier"

    def get_form(self, request, obj=None, **kwargs):    # Just added this override
        form = super(FichecontrolAdmin, self).get_form(request, obj, **kwargs)
        form.user = request.user
        if obj is None:
            if form.base_fields.get('document_signe', None):
                form.base_fields.pop('document_signe')
        return form

    # def response_change(self, request, obj):
    #     return HttpResponseRedirect(reverse('gesco:commercial_fichecontrol_changelist'))
    #     """
    #     Override the response after an object is successfully changed.
    #     """
    #     if "_saveasnew" in request.POST:
    #         # If the user clicked "Save as new," redirect to the add view
    #         return super().response_add(request, obj, post_url_continue='../add/')

    #     # Check if the object still exists
    #     try:
    #         obj = self.get_object(request, obj.pk)
    #     except self.model.DoesNotExist:
    #         # Object does not exist, redirect to a specific page
    #         messages.error(request, _("La fiche de control n'existe pas ou a été tarifié."))
    #         return HttpResponseRedirect(reverse('gesco:commercial_fichecontrol_changelist'))  # Change to your desired URL

    #     return super().response_change(request, obj)

class FicheTarificationAdmin(admin.ModelAdmin):
    form = forms.FicheTarificationAdminForm
    change_form_template = 'admin/commercial/fichetarification/change_form.html'
    list_display = ['numero', 'montant', 'fournisseur', 'fichecontrol_link', 'user', 'date_tarification', 'modified', 'custom_action_button']
    exclude = ['user', 'transferer', 'archived']
    list_filter = ['numero', 'user', 'fichecontrol', 'fichecontrol__fournisseur']

    def save_model(self, request, obj, form, change):
        # Save the Payment model
        super().save_model(request, obj, form, change)
        if not change and not obj.user:  # Check if the object is being created (not updated)
            obj.user = request.user
        if 'a' in request.GET:
            fichecontrol_id = request.GET.get('a')
            # Check if the related object exists
            try:
                fichecontrol = Fichecontrol.objects.get(id=fichecontrol_id)
                obj.fichecontrol = fichecontrol
            except TransferedFicheTarification.DoesNotExist:
                raise Http404(f"La fiche de control correspondante n'existe pas!")

        super().save_model(request, obj, form, change)

    def fournisseur(self, obj):
        return obj.fichecontrol.fournisseur
    
    def montant(self, obj):
        if obj.total_price:
            return  intcomma(obj.total_price,0)
        else:
            return None
    
    def fichecontrol_link(self, obj):
        return format_html('<a href="%s">%s</a>' % (reverse("gesco:commercial_fichecontrol_change", args=(obj.fichecontrol.pk,)), escape(obj.fichecontrol)))

    fichecontrol_link.allow_tags = True
    fichecontrol_link.short_description = "Fiche Control"
    
    def custom_action_button(self, obj):
        transferer_url = reverse('gesco:commercial_tarification_transferer', args=[obj.id])
        generate_pdf_url = reverse('gesco:generate-fichetarification', args=[obj.pk])  # Replace 'generate_pdf' with your actual URL name
        return format_html(
            '<a class="button default" href="{}">Payement</a>'
            '<a class="button" href="{}">Archiver</a>'
            ' <a class="button print-button" href="#" data-url={}>Imprimer</a>',
            transferer_url,
            generate_pdf_url,
            generate_pdf_url,
            generate_pdf_url,
        )

    def response_add(self, request, obj, post_url_continue=None):
        # Check if the 'your_variable' is present in the request
        if 'a' in request.GET and request.method == 'POST' and "_save" in request.POST:
            # If the variable is present, customize the redirect URL
            obj_url = reverse('gesco:commercial_fichetarification_change', args=[obj.pk])
            message = format_html('La fiche tarification « <a href="{}">{}</a> » a été ajouté avec succès.', obj_url, obj)
            self.message_user(request, message, level=messages.SUCCESS)
            return HttpResponseRedirect(reverse('gesco:commercial_fichetarification_changelist') + '?transferer__exact=0')

        # If the variable is not present, use the default redirect URL
        return super().response_add(request, obj, post_url_continue)

    def response_change(self, request, obj):
        # Your existing response_change logic here

        post_url_continue = request.POST.get("_continue", None)
        post_url_addanother = request.POST.get("_addanother", None)

        if not (post_url_continue or post_url_addanother):
            # The user didn't click "Save and continue editing" or "Save and add another"
            # Redirect to a different URL after saving changes
            obj_url = reverse('gesco:commercial_fichetarification_change', args=[obj.pk])
            message = format_html('La fiche tarification « <a href="{}">{}</a> » a été modifié avec succès.', obj_url, obj)
            self.message_user(request, message, level=messages.SUCCESS)
            url = reverse('gesco:commercial_fichetarification_changelist') + '?transferer__exact=0'
            return HttpResponseRedirect(url)

        return super().response_change(request, obj)
    
    custom_action_button.allow_tags = True
    custom_action_button.short_description = 'Actions'  # Set a description for the column

    actions = ['payer', 'mark_as_transfered']  # Add your custom action here
    def mark_as_transfered(self, request, queryset):
        # Update the transfered value to True for selected items
        queryset.update(transferer=True)

    mark_as_transfered.short_description = "Transferer pour paiement"

    # def tarifier(self, request, queryset):
    #     # Perform your custom action here
    #     selected_ids = queryset.values_list('id', flat=True)
    #     # Do something with selected_ids

    # tarifier.short_description = 'Payer'

    # def get_queryset(self, request):
    #     # Get the original queryset
    #     queryset = super().get_queryset(request)

    #     queryset = queryset.exclude(transferer=True)
    #     return queryset

    def get_form(self, request, obj=None, **kwargs):
        form = super(FicheTarificationAdmin, self).get_form(request, obj, **kwargs)

        if obj is None:
            if form.base_fields.get('document_signe', None):
                form.base_fields.pop('document_signe')

        fichecontrol_id = request.GET.get('a')
        # Check if the related object exists
        if fichecontrol_id:
            try:
                fichecontrol = Fichecontrol.objects.get(id=fichecontrol_id)
                # form.fichecontrol = fichecontrol
                form.base_fields['fichecontrol'].initial = fichecontrol
            except TransferedFicheTarification.DoesNotExist:
                raise Http404(f"La fiche de control correspondante n'existe pas!")

        form.user = request.user
        return form


class FichePaiementAdmin(FicheTarificationAdmin):
    pass

class ControlLingotAdmin(admin.ModelAdmin):
    inlines=[PourcentageSubstanceControlLingotInline]
    change_form_template = 'admin/commercial/controllingot/change_form.html'
    formset = forms.ControlInlineFormSet

    fieldsets = [
        (None, {'fields': ['numero', 'type_de_control', 'control', 'user', 'numero_lingot_control', 'observation']}),  # Include your model fields here
        ('Poids',  {'fields': ['poids_brut', 'poids_immerge', 'titre_carat', 'or_fin', 'ecart', 'densite'], 'classes': ['collapse']}),
    ]

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)

        if obj:
            print('ControlLingotAdmin::get_formet():::form.fields', form.fields)
            # Set the initial value for the inline field based on the parent model
            for form in formset.forms:
                form.fields['lingot'].initial = obj.lingot  # Adjust 'inline_field' to your actual field name

        return formset

class ControlAdmin(admin.ModelAdmin):
    form = forms.ControlAdminForm
    inlines=[ControlLingotInline]
    exclude = ['user']
    fields = ['date_control', 'type_de_control', 'control_client', 'structure_de_control', 'vente', 'observation', 'lingots', 'document_signe', 'numero_de_control']
    readonly_fields = ['numero_de_control']

    def get_fields(self, request, obj=None):
        # Check if the instance is a new object
        if not obj:
            type_de_control = request.GET.get('t', None)
            if type_de_control and type_de_control == "affinage":
                return ['date_control', 'type_de_control', 'control_client', 'structure_de_control', 'vente', 'observation', 'lingots', 'numero_de_control']
            else:
                return ['date_control', 'type_de_control', 'vente', 'observation', 'lingots', 'numero_de_control']
        else:
            # If editing an existing object, include all fields
            return super().get_fields(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        # Customize the form based on GET parameters
        form = super(ControlAdmin, self).get_form(request, obj, **kwargs)
        # form = super().get_form(request, obj, **kwargs)

        # Check if it's an add action or a change action
        if obj is None:
            type_de_control = request.GET.get('t', None)
            if type_de_control:
                print('type control:', type_de_control)
                if not type_de_control in [key for key, value in TYPE_CONTROL]:
                    message = "Ce type de control n'est pas defini!"
                    self.message_user(request, format_html(message), level='ERROR')
                    return form
                form.base_fields['type_de_control'].disabled = True
            else:
                type_de_control = 'bumigeb'
            form.base_fields['type_de_control'].initial = type_de_control


            vente_id = request.GET.get('v', None)
            vente = None
            if vente_id:
                try:
                    vente = Vente.objects.get(id=vente_id)
                    print('Vente.objects.get(id=vente_id):::', vente)
                    form.base_fields['vente'].initial = vente
                    form.base_fields['vente'].disabled = True
                    form.base_fields['vente'].widget.can_add_related = False
                    form.base_fields['lingots'].initial = Lingot.objects.filter(
                        vente=vente
                    )
                except Vente.DoesNotExist as e:
                    # Model not found, handle the exception
                    error_message = f"Erreur! Une exception de type: {type(e).__name__}: Vente non existant: {str(e)}"
                    self.message_user(request, error_message, level=messages.ERROR)
                    
                    # Redirect to the referrer or any specific URL
                    referer = request.META.get('HTTP_REFERER')
                    redirect(referer or reverse('gesco:index'))
                except Exception as e:
                    # Catch a general exception and inform the user about the type
                    error_message = f"Une erreur de type: {type(e).__name__} s'est produite: {str(e)}"
                    self.message_user(request, error_message, level=messages.ERROR)
                    
                    # Redirect to the referrer or any specific URL
                    referer = request.META.get('HTTP_REFERER')
                    redirect(referer or reverse('gesco:index'))
                # form.base_fields['vente'].initial = vente
                # form.base_fields['vente'].disabled = True
                # form.base_fields['vente'].widget.can_add_related = False
                return form
            else:
                

                #new part
                lingot_ids = request.GET.getlist('l', [])
                initial_lingots = Lingot.objects.filter(pk__in=lingot_ids)

                if not len(initial_lingots) > 0:
                    error_message = 'Veuillez selectionner des lingots pour le control'
                    self.message_user(request, error_message)
                    return form
                form.base_fields['lingots'].initial = initial_lingots

                all_lingots_to_control = None
                lingots_without_control = initial_lingots.filter(
                    controllingot__isnull=True
                ).distinct()
                lingots_to_control = initial_lingots.exclude(
                    controllingot__type_de_control=type_de_control,
                ).distinct()
                all_lingots_to_control = lingots_without_control | lingots_to_control

                if not all_lingots_to_control or not len(all_lingots_to_control) > 0:
                    error_message = "Veuillez selectionner des lingots valides n'ayant pas encore fait l'objet de cet type de control"
                    self.message_user(request, error_message)
                    return form

        return form

    def save_model(self, request, obj, form, change):
        # Save the MouvementLingot model
        if not form.is_valid():
            self.message_user(request, "L'opération a échoué. Certains données sont invalides!")
            return

        if not obj.pk:
            obj.user = request.user
        super().save_model(request, obj, form, change)


        lingots = form.cleaned_data.get('lingots', None)

        print("form.cleaned_data.get('lingots', None):::", lingots)
        if lingots and len(lingots) > 0:
            # Dissocier les control lingots qui ne sont pas dans le nouveau ensemble
            obj.controllingot_set.exclude(lingot__in=lingots).update(control=None)
            print("obj.controllingot_set.exclude(lingot__in=lingots):::", obj.controllingot_set.exclude(lingot__in=lingots))

            # Selectionner les controllingot deja existants dont le type de control correspond a ce type de control et les associé a ce control
            ControlLingot.objects.filter(
                lingot__in = lingots,
                type_de_control=obj.type_de_control
            ).update(
                control=obj,
            )

            print("ControlLingot.objects.filter(:::", ControlLingot.objects.filter(lingot__in = lingots,type_de_control=obj.type_de_control))

            # Selectionner les nouveau lingots sans control et creer des controls
            lingots = lingots.exclude(
                id__in=obj.controllingot_set.all().values_list('lingot', flat=True),
                controllingot__type_de_control=obj.type_de_control
            ).distinct()

            print(
                "id__in=obj.controllingot_set.all().values_list('lingot', flat=True):::", lingots)

            # Creer des controls lingots pour ces lingots
            for lingot in lingots:
                control_lingot = ControlLingot.objects.create(
                    lingot=lingot,
                    control=obj,
                    type_de_control=obj.type_de_control,
                    user=request.user,
                    poids_brut=lingot.poids_brut
                    )
                control_lingot.save()


    def response_add(self, request, obj, post_url_continue=None):
        # Check if the 'your_variable' is present in the request
        if request.GET.get('v', None) and request.GET.get('t', None):
            # If the variable is present, customize the redirect URL
            return HttpResponseRedirect(reverse('gesco:commercial_control_change', args=[obj.pk]))
        # If the variable is not present, use the default redirect URL
        return super().response_add(request, obj, post_url_continue)

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3})},
    }

class RapportAffiangeAdmin(ControlAdmin):
    model = RapportAffinage
    # form = forms.ControlBUMIGEBAdminForm
    # inlines = [PourcentageSubstanceRapportAffinageInline]
    # list_display = ['numero', 'client', 'date', 'user', 'etat', 'custom_actions']
    show_change_link = True


    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3})},
    }

    def response_change(self, request, obj):
        if 'rt' in request.GET and obj.etat == 'in':
            return HttpResponseRedirect(reverse('gesco:commercial_vente_changelist') + '?conclu__exact=0')
        return super().response_change(request, obj)



class LingotAdmin(admin.ModelAdmin):
    form = forms.LingotAdminForm
    inlines = [PeseeInLineAdmin, PourcentageSubstanceLingotInline]
    list_display = ['numero', 'fournisseur', 'fichecontrol', 'numero_bumigeb', 'control_bumigeb', 'user', 'date_reception', 'custom_action_button']
    exclude = ['user']
    readonly_fields = ['user', 'poids_brut', 'poids_immerge', 'ecart', 'densite', 'titre', 'or_fin']
    # fields = ['date_reception', 'observation',  'poids_brut', 'poids_immerge', ('ecart', 'densite'), ('titre', 'or_fin')]
    list_filter = ['numero', 'fournisseur', 'fichecontrol', 'numero_bumigeb', LingotControlBUMIGEBFilter, 'user', 'titre', IsMeltedFilter, 'vente__conclu']

    fieldsets = [
        (None, {'fields': ['fournisseur', 'date_reception', 'observation']}),  # Include your model fields here
        ('Poids',  {'fields': ['poids_brut', 'poids_immerge', ('ecart', 'densite'), ('titre', 'or_fin')], 'classes': ['collapse']}),
    ]

    inline_type = 'tabular'
    insert_after = 'pesees'

    def custom_action_button(self, obj):
        return format_html('<a class="button" href="#">Voir</a> <a class="button default" href="#">Imprimer</a>')


    # def get_list_display(self, request):
    #     # Conditionally include 'conditionally_displayed_field' based on the URL name
    #     if request.resolver_match.url_name == 'vente_lingot_changelist':
    #         self.list_display = ['numero', 'fournisseur', 'user', 'fichecontrol', 'date_reception', 'modified', 'custom_action_button_vente']
    #     return super().get_list_display(request)

    custom_action_button.allow_tags = True
    custom_action_button.short_description = 'Actions'  # Set a description for the column

    actions = ['fondre', 'control_BUMIGEB', 'avendre', 'deplacer_vers_emplacement']  # Add your custom action here

    def get_queryset(self, request):
        return stock_queryset(queryset=super().get_queryset(request))

    def get_filters_params(self, request, *args, **kwargs):
        params = super().get_filters_params(request, *args, **kwargs)

        # Set a default value for the custom filter if it's not present in the request
        if 'is_melted' not in params:
            params['is_melted'] = 'no'
        return params

    def fondre(self, request, queryset):

        already_linked_items = queryset.filter(fonte__isnull=False)

        if already_linked_items.exists():
            # Display an error message for already linked items
            error_message = "Erreur, les lingots suivants sont deja fondus:"
            for item in already_linked_items:
                error_message += f"<br>{item} --> Fonte: {item.fonte}"
            self.message_user(request, format_html(error_message), level='ERROR')
            return

        # Create a new instance of LinkedModel
        fonte = Fonte.objects.create(user=request.user)

        for lingot in queryset:

            lingot.fonte = fonte
            lingot.save()

        # Get the URL of the LinkedModel instance
        linked_model_url = reverse(
            'gesco:commercial_fonte_change', args=[fonte.id]
        )

        message = f'Total de {queryset.count()} lingots envoyés en fonte No <a href="{linked_model_url}">{fonte}</a>'

        self.message_user(request, format_html(message))

    fondre.short_description = 'Fondre la selection'

    def deplacer_vers_emplacement(self, request, queryset):

       # Create a list of primary keys of the selected ModelB instances
        lingot_ids_list = list(queryset.values_list('pk', flat=True))
        lingot_ids = '&l='.join(map(str, queryset.values_list('pk', flat=True)))

        # Redirect to the add form for ModelA with the initial values
        mouvement_add_url = reverse('gesco:commercial_mouvementlingot_add') + f'?l={lingot_ids}'
        return HttpResponseRedirect(mouvement_add_url)

        self.message_user(request, format_html("Les lingots ont étés deplacés"))

    deplacer_vers_emplacement.short_description = "Deplacer vers un emplacment"

    fondre.short_description = 'Fondre la selection'

    def control_BUMIGEB(self, request, queryset):

        already_linked_items = queryset.filter(control_bumigeb__isnull=False)

        if already_linked_items.exists():
            # Display an error message for already linked items
            error_message = "Echec, les lingots suivants sont deja controllé:"
            for item in already_linked_items:
                error_message += f"<br>{item} --> Control: {item.control_bumigeb}"
            self.message_user(request, format_html(error_message), level='ERROR')
            return

        # Create a new instance of LinkedModel
        control_bumigeb = ControlBUMIGEB.objects.create(user=request.user)

        for lingot in queryset:

            lingot.control_bumigeb = control_bumigeb
            lingot.save()


        # Get the URL of the LinkedModel instance
        linked_model_url = reverse(
            'gesco:commercial_controlbumigeb_change', args=[control_bumigeb.id]
        )

        message = f'Total de {queryset.count()} lingots envoyés pour control BUMIGEB No <a href="{linked_model_url}">{control_bumigeb}</a>'

        self.message_user(request, format_html(message))

    control_BUMIGEB.short_description = 'Envoyer la selection pour control BUMIGEB'

    def avendre(self, request, queryset):
        # Custom action logic to set your_boolean_field to True
        queryset.update(avendre=True)

    avendre.short_description = 'Disponibiliser pour la vente'

    control_BUMIGEB.short_description = 'Sortir la selection pour control BUMIGEB'

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        if 'ft' in request.GET:
            extra_context['show_save_and_add_another'] = False
            extra_context['show_save_and_continue'] = False
        return super().add_view(request, form_url, extra_context=extra_context)
    
    def get_readonly_fields(self, request, obj=None):
        # Check if a specific parameter is present in the request
        if 'ft' in request.GET:
            # Make fields editable based on the parameter value
            editable_fields = request.GET.getlist('editable_fields')
            readonly_fields = ['user', 'ecart', 'densite', 'titre', 'or_fin', 'date_reception']
            return readonly_fields

        # Default to the original readonly_fields
        return super().get_readonly_fields(request, obj)

    def get_fields(self, request, obj=None):
        # Check if a specific parameter is present in the request
        if 'ft' in request.GET:
            # Extract field names from the parameter value
            fields = ['poids_brut', 'poids_immerge', 'observation', ('ecart', 'densite'), ('titre', 'or_fin'),]
            # Filter the original fields based on the parameter value
            return fields

        # Default to the original set of fields
        return super().get_fields(request, obj)


    def response_add(self, request, obj, post_url_continue=None):
        # Check if the 'your_variable' is present in the request
        if 'ft' in request.GET and request.method == 'POST' and "_save" in request.POST:
            # If the variable is present, customize the redirect URL
            return HttpResponseRedirect(reverse('gesco:commercial_fonte_changelist') + '?/etat__exact=in')

        if 'ft' in request.GET and request.method == 'POST' and "_save" in request.POST:
            # If the variable is present, customize the redirect URL
            return HttpResponseRedirect(reverse('gesco:commercial_fonte_changelist') + '?/etat__exact=in')

        # If the variable is not present, use the default redirect URL
        return super().response_add(request, obj, post_url_continue)

    def get_form(self, request, obj=None, **kwargs):
        # Customize the form based on GET parameters
        form = super().get_form(request, obj, **kwargs)


        # Check if a parameter is present in the request
        if 'ft' in request.GET:
            fonte_id = request.GET['ft']
            kwargs['form'] = forms.LingotAdminForm
            # Remove the specified field from the form

        return form

    def save_model(self, request, obj, form, change):
        # Save the Payment model
        if not form.is_valid():
            self.message_user(request, "L'operation a echouée. Erreur interne!")
            return

        if not change and not obj.user:  # Check if the object is being created (not updated)
            obj.user = request.user


        # Check if the related object exists
        if 'ft' in request.GET:
            fonte_id = request.GET.get('ft')
            fonte = Fonte.objects.get(id=fonte_id)
            if not fonte:
                self.message_user(request, "L'operation a echouée. Erreur interne!")
                return


            if fonte.fondu:
                messages.set_level(request, messages.ERROR)
                messages.error(request, "L'operation a echouée. fonte deja validé")
                return

            obj.is_fonte = True
            obj.save()

            try:
                with transaction.atomic():
                    lingot_fondu = LingotFondus.objects.create(fonte=fonte, lingot=obj, user=request.user)
                    lingot_fondu.save()
            except Exception as e:
                messages.error(request, f"Erreur interne lors de la validation de la fonte: {e}")
                return

            fonte.date_retour = timezone.now()
            fonte.fondu = True
            fonte.etat = 'in'
            fonte.valider_par = request.user
            fonte.save(update_fields=['date_retour', 'fondu', 'etat'])
            messages.add_message(request, messages.SUCCESS, "Operation reussi!")
        else:
            super().save_model(request, obj, form, change)

class TransferedLingotAdmin(admin.ModelAdmin):
    list_display = ['numero', 'source', 'destination', 'fournisseur', 'numero_bumigeb', 'control_bumigeb', 'user', 'date_reception', 'custom_actions']
    list_filter = ['numero', 'fournisseur', 'fichecontrol', 'numero_bumigeb', LingotControlBUMIGEBFilter, 'user', 'titre', IsMeltedFilter, 'vente__conclu']

    def destination(self, obj):
        latest_move = None
        try:
            latest_move = MouvementLingot.objects.filter(
                lingots__id=obj.pk,
                mouvementlingotlingot__moved=False
            ).order_by('-date_deplacement').first()
        except:
            pass
        if latest_move:
            return f"{latest_move.destination}"
        else:
            return "-"

    def source(self, obj):
        previous_location = None
        try:
            previous_location = MouvementLingot.objects.filter(
                lingots__id=obj.pk,
                mouvementlingotlingot__moved=True,
                etat='end'
            ).order_by('-date_deplacement').first()
        except:
            pass
        if previous_location:
            return f"{previous_location.destination}"
        else:
            return "STOCK"

    def custom_actions(self, obj):
        history_url = reverse('gesco:commercial_mouvementlingot_changelist') + f'?mouvementlingotlingot__lingot_id={obj.pk}'
        return format_html('<a class="button" href="{}">Historique</a>', history_url)

    def deplacer_vers_emplacement(self, request, queryset):

       # Create a list of primary keys of the selected ModelB instances
        lingot_ids_list = list(queryset.values_list('pk', flat=True))
        lingot_ids = '&l='.join(map(str, queryset.values_list('pk', flat=True)))

        # Redirect to the add form for ModelA with the initial values
        mouvement_add_url = reverse('gesco:commercial_mouvementlingot_add') + f'?l={lingot_ids}'
        return HttpResponseRedirect(mouvement_add_url)

        self.message_user(request, format_html("Les lingots ont étés deplacés"))

    deplacer_vers_emplacement.short_description = "Deplacer vers un emplacment"

    def marque_reached_destination(self, request, queryset):
        # Update the transfered value to True for selected items
        MouvementLingot.objects.filter(lingots__in=queryset).update(etat='end')

    marque_reached_destination.short_description = "Marquer comme arrivé a destination"

    actions = ['deplacer_vers_emplacement', 'marque_reached_destination']

    def get_actions(self, request):
        actions = super().get_actions(request)
        del actions['delete_selected']
        return actions


class LingotsDisponiblesPourVenteAdmin(admin.ModelAdmin):
    list_display = ['numero', 'numero_bumigeb', 'fournisseur', 'user', 'fichecontrol', 'date_reception', 'modified', 'custom_actions']

    # def lingot(self, obj):
    #     try:
    #         lingot_resultant = Lingot.objects.get(control_bumigeb=obj)
    #     except:
    #         return '-'
    #     url_lingot_resultant = reverse('gesco:commercial_lingot_change', args=[lingot_resultant.pk])
    #     return format_html('<a href="{}">{}</a>', url_lingot_resultant, lingot_resultant)
    list_filter = [LingotControlBUMIGEBFilter, 'fichecontrol']

    def vendre(self, request, queryset):
        already_linked_items = queryset.filter(vente__isnull=False)



        if already_linked_items.exists():
            # Display an error message for already linked items
            error_message = "Echec, les lingot(s) suivant(s) sont deja associé(s) a une vente:"
            for item in already_linked_items:
                error_message += f"<br>{item} --> Vente No. {item.vente}"
            self.message_user(request, format_html(error_message), level='ERROR')
            return

        # Create a list of primary keys of the selected ModelB instances
        lingot_ids = '&l='.join(map(str, queryset.values_list('pk', flat=True)))

        # Redirect to the add form for ModelA with the initial values
        vente_add_url = reverse('gesco:commercial_vente_add') + f'?l={lingot_ids}&t=bumigeb'
        return HttpResponseRedirect(vente_add_url)

        # Create a new instance of LinkedModel
        vente = Vente.objects.create(user=request.user, date=timezone.now())

        for lingot in queryset:

            lingot.vente = vente
            lingot.save()


        # Get the URL of the LinkedModel instance
        linked_model_url = reverse(
            'gesco:commercial_vente_change', args=[vente.pk]
        )

        message = f'Total de {queryset.count()} lingots selectionner pour vente No. <a href="{linked_model_url}">{vente}</a>'

        self.message_user(request, format_html(message), level="SUCCESS")
        return HttpResponseRedirect(reverse(
            'gesco:commercial_vente_change', args=[vente.pk]
        ))

    vendre.short_description = "Vendre la selection"

    def novendre(self, request, queryset):
        # Custom action logic to set your_boolean_field to True
        queryset.update(avendre=False)

    novendre.short_description = 'Retirer du stock a vendre'

    # def facture_proforma(self, request, queryset):
    #     already_linked_items = queryset.filter(facture_proforma__isnull=False)

    #     if already_linked_items.exists():
    #         # Display an error message for already linked items
    #         error_message = "Echec, les lingots suivants ont deja une facture proforma:"
    #         for item in already_linked_items:
    #             error_message += f"<br>{item} --> Facture proforma: {item.facture_proforma}"
    #         self.message_user(request, format_html(error_message), level='ERROR')
    #         return

    #     # Create a new instance of LinkedModel
    #     factureproforma = FactureProforma.objects.create(user=request.user, date=timezone.now())

    #     for lingot in queryset:

    #         lingot.facture_proforma = factureproforma
    #         lingot.save()


    #     # Get the URL of the LinkedModel instance
    #     linked_model_url = reverse(
    #         'gesco:commercial_factureproforma_change', args=[factureproforma.pk]
    #     )

    #     message = f'Total de {queryset.count()} lingots ajouté a la facture proforma <a href="{linked_model_url}">{factureproforma}</a>'

    #     self.message_user(request, format_html(message), level="SUCCESS")

    # facture_proforma.short_description = "Creer une facture proforma pour la selection"

    # def facture_definitive(self, request, queryset):
    #     pass

    def custom_actions(self, obj):
        # url_add_proforma = reverse('gesco:commercial_factureproforma_add')
        return format_html('<a class="button" href="#">Voir</a> <a class="button default" href="">Proforma</a>')

    custom_actions.short_description = 'Actions'  # Set a description for the column

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3})},
    }

    actions = ['vendre', 'facture_proforma', 'facture_definitive', 'novendre']

    # facture_definitive.short_description = "Creer une facture definitive pour la selection"

    def get_actions(self, request):
        actions = super().get_actions(request)
        del actions['delete_selected']
        return actions




class FournisseurAdmin(admin.ModelAdmin):
    inlines = [LingotInLineAdmin]
    list_display = ['nom', 'prenom', 'email', 'telephone', 'solde', 'type_fournisseur', 'custom_action_button']
    exclude = []

    add_form_template = 'commercial/admin/fournisseur/add.html'

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3})},
    }

    def solde(self, obj):
        fcs = Fichecontrol.objects.filter(fournisseur=obj).values('id')
        fts = FicheTarification.objects.filter(fichecontrol__isnull=False, fichecontrol_id__in=fcs, transferer=True)
        pys = Payement.objects.filter(fichetarification_id__in=fts.values('id'))
        total_price = sum(ft.total_price for ft in fts)
        total_reste = sum(py.montant for py in pys)
        tot = Decimal(round(Decimal(total_price - total_reste), 0))
        return intcomma(tot).replace(',', ' ')


    def custom_action_button(self, obj):
        url = reverse('gesco:commercial_smsfournisseur_add')
        sms = format_html('<a class="button default" href="{}?f={}">ENVOYER SMS</a>', url, obj.id)
        # actions = format_html(' <a class="button" href="#">Imprimer</a> ')
        return sms

    custom_action_button.allow_tags = True
    custom_action_button.short_description = 'Actions'  # Set a description for the column

    def envoie_message(self, request, queryset):

         # Create a list of primary keys of the selected ModelB instances
        user_ids = '&f='.join(map(str, queryset.values_list('pk', flat=True)))

        # Redirect to the add form for ModelA with the initial values
        add_sms_url = reverse('gesco:commercial_smsfournisseur_add') + f'?f={user_ids}'
        return HttpResponseRedirect(add_sms_url)

    actions = ['envoie_message']
    envoie_message.short_description = "Envoyer un message a la selection"

class PayementAdmin(admin.ModelAdmin):
    form = forms.PayementAdminFrom
    list_display = ['numero', 'user', 'fournisseur', 'fiche_tarification', 'montant_paye', 'resteapayer', 'custom_actions']
    
    exclude = ['direction', 'user', 'archived', 'actif', 'confirmed', 'fichetarification']
    readonly_fields = ['user', 'fournisseur', 'numero']

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3})},
    }
    def fournisseur(self, obj):
        return obj.fichetarification.fichecontrol.fournisseur

    def resteapayer(self, obj):
        val = Decimal(obj.reste_a_payer)
        return intcomma(val)
    
    resteapayer.short_description = 'Reste a payer'
    resteapayer.short_description = 'Reste a payer'

    def montant_paye(self, obj):
        return intcomma(obj.montant) if obj.montant else 0


    def fiche_tarification(self, obj):
        url_ft = reverse('gesco:commercial_fichetarification_change', args=[obj.fichetarification.pk])
        return format_html('<a href="{}">{}</a>', url_ft, obj.fichetarification)

    fiche_tarification.short_description = "Fiche Tarification"

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not obj is None and not obj.user:
            form.user = request.user

        if obj is None:
            if form.base_fields.get('recu_payement', None):
                form.base_fields.pop('recu_payement')

        if 'a' in request.GET:
            fichetarification_id = request.GET.get('a')
            # Check if the related object exists
            try:
                fichetarification = TransferedFicheTarification.objects.get(id=fichetarification_id)
                form.base_fields['montant'].initial = fichetarification.reste_a_payer
            except TransferedFicheTarification.DoesNotExist:
                raise Http404(f"La fiche de tarification correspondante n'existe pas!")

        return form

    actions = ["archiver"]



    def archiver(self, request, queryset):
        # Custom action logic to set your_boolean_field to True
        queryset.update(archived=True)

    archiver.short_description = "Archiver la selection"

    # capture the request object to retrieve the GET parameters
    is_archived_filter = None
    request = None
    def changelist_view(self, request, extra_context=None):
        self.request = request
        self.is_archived_filter = request.GET.get('archived__exact') == '1'
        return super().changelist_view(request, extra_context=extra_context)


    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<path:object_id>/archiver/', self.admin_site.admin_view(commercial_payement_archiver_view), name='commercial_payement_archiver'),
        ]
        return custom_urls + urls


    def custom_actions(self, obj):
        class_name = 'disabled-link' if self.is_archived_filter else ''


        url = reverse('gesco:commercial_payement_archiver', args=[obj.id])
        url_generer_recu = reverse('gesco:generate_recu_payement_achat', args=[obj.id])
        generation_button = format_html('<a class="button default print-button {}" href="#" data-url={}>Gen. Recu</a> ', class_name, url_generer_recu)
        print_button = format_html('<a class="button {}" href="{}">Archiver</a>', class_name, url)

        return generation_button + print_button

    custom_actions.allow_tags = True

    def response_add(self, request, obj, post_url_continue=None):
        # Check if the 'your_variable' is present in the request
        if 'a' in request.GET and request.method == 'POST' and "_save" in request.POST:
            # If the variable is present, customize the redirect URL
            return HttpResponseRedirect(reverse('gesco:commercial_payement_changelist') + '?archived__exact=0')

        # If the variable is not present, use the default redirect URL
        return super().response_add(request, obj, post_url_continue)

    def save_model(self, request, obj, form, change):
        # Save the Payment model
        super().save_model(request, obj, form, change)

        if not change and not obj.user:  # Check if the object is being created (not updated)
            obj.user = request.user

        if 'a' in request.GET:
            fichetarification_id = request.GET.get('a')
            # Check if the related object exists
            try:
                fichetarification = TransferedFicheTarification.objects.get(id=fichetarification_id)
                obj.fournisseur = fichetarification.fichecontrol.fournisseur
                obj.fichetarification = fichetarification
            except TransferedFicheTarification.DoesNotExist:
                raise Http404(f"La fiche de tarification correspondante n'existe pas!")



        super().save_model(request, obj, form, change)

class PayementCompletFilter(admin.SimpleListFilter):
    title = _('Complet/Imcomplet')
    parameter_name = 'payement_complet'

    def lookups(self, request, model_admin):
        return (
            ('positive', _('Complet')),
            ('negative', _('Imcomplet')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'positive':
            return [obj for obj in queryset if obj.reste_a_payer > 0]
        elif self.value() == 'negative':
            return [obj for obj in queryset if obj.reste_a_payer < 0]
        else:
            return queryset

class TransferedFicheTarificationAdmin(admin.ModelAdmin):
    list_display = ['numero', 'fichecontrol_link', 'fournisseur', 'montant', 'resteapayer', 'user', 'custom_action_button']  # Add your actual fields here

    list_filter = [PayementCompletFilter]
    def custom_action_button(self, obj):
        url = reverse('gesco:commercial_payement_add')
        return format_html('<a class="button default" href="{}?a={}">Payer</a>', url, obj.id)
        # return format_html('<a class="button default" href="#">Payer</a>')

    def montant(self, obj):
        val = Decimal(obj.total_price)
        return intcomma(val)

    def resteapayer(self, obj):
        val = Decimal(obj.reste_a_payer)
        return intcomma(val)

    def fournisseur(self, obj):
        return obj.fichecontrol.fournisseur
    
    def fichecontrol_link(self, obj):
        return format_html('<a href="%s">%s</a>' % (reverse("gesco:commercial_fichecontrol_change", args=(obj.fichecontrol.pk,)), escape(obj.fichecontrol)))

    fichecontrol_link.allow_tags = True
    fichecontrol_link.short_description = "Fiche Control"

    actions = ["renvoyer_en_tarification"]

    def renvoyer_en_tarification(self, request, queryset):
        queryset.update(transferer=False)

        self.message_user(request, f'Les fiches ont étées renvoyé en tarification avec succès!')

    renvoyer_en_tarification.short_description = "Renvoyer la selection en tarification"


    montant.shord_description = 'Total a payer'
    custom_action_button.allow_tags = True
    custom_action_button.short_description = 'Actions'  # Set a description for the column


class VenteAdmin(admin.ModelAdmin):
    form = forms.VenteAdminForm
    inlines = [FactureProformaInlineAdmin, RapportAffinageInlineAdmin, FactureDefinitiveInlineAdmin]
    model = Vente
    list_display = ['numero', 'client', 'vendre_selon', 'user', 'action_proforma', 'action_rapport', 'action_definitive']
    exclude = [
        'user', 'date_retour', 'etat', 'date_conclusion' 'archived', 'reintegrer_par', 'conclu',
        'date', 'archive'
    ]
    show_change_link = True
    fields = [ 'numero', 'client', 'vendre_selon', 'objet', 'observation', 'lingots', 'controls']
    readonly_fields = ['numero']


    # def montant(self, obj):
    #     if obj.facture_definitive and obj.facture_definitive.montant():
    #         return obj.facture_definitive.montant()
    #     elif obj.facture_proforma and obj.facture_proforma.montant():
    #         return obj.facture_proforma.montant()
    #     else:
    #         return None

    def action_proforma(self, obj):
        facture_proforma = FactureProforma.objects.filter(vente=obj).first()
        if facture_proforma:
            proforma_text = 'Editer Proforma'
            proforma_url = reverse('gesco:commercial_factureproforma_change', args=[facture_proforma.pk])
            proforma_class_name = ''
        else:
            proforma_text = 'CREER PROFORMA'
            proforma_url = reverse('gesco:commercial_factureproforma_add') + f'?v={obj.pk}&t=proforma'
            proforma_class_name = ''
        return format_html('<a class="button {}" href="{}">{}</a>', proforma_class_name, proforma_url, proforma_text)

    def action_definitive(self, obj):
        facture_definitive = FactureDefinitive.objects.filter(vente=obj).first()
        if facture_definitive:
            definitive_text = 'Editer definitive'
            definitive_url = reverse('gesco:commercial_facturedefinitive_change', args=[facture_definitive.pk])
            definitive_class_name = ''
        else:
            definitive_text = 'CREER definitive'
            definitive_url = reverse('gesco:commercial_facturedefinitive_add') + f'?v={obj.pk}&t=definitive'
            definitive_class_name = ''
        return format_html('<a class="button {}" href="{}">{}</a>', definitive_class_name, definitive_url, definitive_text)

    def action_rapport(self, obj):
        rapport_affinage = RapportAffinage.objects.filter(vente=obj).first()
        if rapport_affinage:
            affinage_text = 'Editer Rapport'
            affinage_url = reverse('gesco:commercial_rapportaffinage_change', args=[rapport_affinage.pk])
            affinage_class_name = ''
        else:
            affinage_text = 'Ajouter Rapport'
            affinage_url = reverse('gesco:commercial_control_add') + f'?v={obj.pk}&t=affinage'
            affinage_class_name = ''
        return format_html(' <a class="button default {}" href="{}">{}</a>', affinage_class_name, affinage_url, affinage_text)


    action_definitive.short_description = 'Facture'
    action_proforma.short_description = 'Proforma'
    action_rapport.short_description = 'Rapport Aff.'

    def custom_actions(self, obj):
        url = self.action_proforma(obj)
        url += self.action_rapport(obj)
        url += self.action_definitive(obj)
        # url += self.action_rapport(obj)
        # url += self.action_definitive(obj)
        return url

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3})},
    }

    def get_form(self, request, obj=None, **kwargs):
        # Customize the form based on GET parameters
        form = super(VenteAdmin, self).get_form(request, obj, **kwargs)
        # form = super().get_form(request, obj, **kwargs)

        # Check if it's an add action or a change action
        if obj is None:
            # Add action: prefill with request.GET.getlist('lingots')
            lingot_ids = request.GET.getlist('l', [])
            initial_lingots = Lingot.objects.filter(pk__in=lingot_ids)
            form.base_fields['lingots'].initial = initial_lingots

            vendre_selon = request.GET.get('t', None)

            if vendre_selon:
                form.base_fields['vendre_selon'].initial = vendre_selon
                # form.base_fields['vendre_selon'].disabled = True
                not_controlled_lingots = initial_lingots.exclude(
                    controllingot__control__type_de_control=vendre_selon
                ).distinct()

                if not len(not_controlled_lingots) == 0:
                    # Redirect to the add form for ModelA with the initial values
                    params = '&l='.join(map(str, not_controlled_lingots.values_list('pk', flat=True)))
                    url_create_control = reverse('gesco:commercial_control_add') + f'?l={params}&t={vendre_selon}'
                    list_lingots = ''
                    for l in not_controlled_lingots:
                        list_lingots += f'<br>{l}'

                    message_ajout_control = format_html(
                        f"Ces lingots n'ont pas encore fait l'objet de control: {dict(TYPE_CONTROL).get(vendre_selon)}<br>"
                        f'{list_lingots}<br><a target="blank" class="button" href={url_create_control}>Faire le control pour ces lingot</a>',
                    )
                    self.message_user(request, message_ajout_control, level='ERROR')

                controls_lingot = Control.objects.filter(
                    type_de_control=vendre_selon,
                    controllingot__lingot__in=initial_lingots
                )
                form.base_fields['controls'].initial = controls_lingot.distinct('id')
                form.base_fields['controls'].disabled = True

        return form


    def get_readonly_fields(self, request, obj=None):
        read_only_fields = super().get_readonly_fields(request, obj)
        if obj and obj.conclu:
            read_only_fields = [field.name for field in self.model._meta.get_fields()]
        # Get all field names of the model
        return read_only_fields

class VentesConcluAdmin(admin.ModelAdmin):
    list_display = ['user', 'fournisseur', 'numero', 'montant', 'resteapayer', 'custom_action_button']  # Add your actual fields here

    def custom_action_button(self, obj):
        url = reverse('gesco:commercial_ventesconclu_add')
        return format_html('<a class="button default" href="{}?a={}">Imprimer</a>', url, obj.id)
        # return format_html('<a class="button default" href="#">Payer</a>')

    def montant(self, obj):
        return 0

    def resteapayer(self, obj):
        return 0

    def fournisseur(self, obj):
        return obj.fournisseur

    actions = ["Archiver"]

    def archiver(self, request, queryset):
        queryset.update(archived=True)

        self.message_user(request, f'Les fiches ont étées renvoyé en tarification avec succès!')

    archiver.short_description = "Archiver la selection"


    montant.shord_description = 'Total a payer'
    custom_action_button.allow_tags = True
    custom_action_button.short_description = 'Actions'  # Set a description for the column

class FactureAdmin(admin.ModelAdmin):
    form = forms.FactureAdminForm
    list_display = ['numero', 'user', 'client', 'montant', 'resteapayer', 'custom_action_button']  # Add your actual fields here
    exclude = ['user', 'archived']
    readonly_fields = ['numero']
    change_form_template = 'admin/commercial/facture/change_form.html'
    # form = forms.FactureProformaAdminForm
    def custom_action_button(self, obj):
        url = reverse('gesco:commercial_ventesconclu_add')
        return format_html('<a class="button default" href="{}?a={}">Imprimer</a>', url, obj.id)
        # return format_html('<a class="button default" href="#">Payer</a>')

    def montant(self, obj):
        return 0

    def resteapayer(self, obj):
        return 0

    def client(self, obj):
        return obj.vente.client

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3})},
    }

    actions = ["Archiver"]

    def archiver(self, request, queryset):
        queryset.update(archived=True)

        self.message_user(request, f'Les fiches ont étées renvoyé en tarification avec succès!')

    archiver.short_description = "Archiver la selection"


    montant.shord_description = 'Total a payer'
    custom_action_button.allow_tags = True
    custom_action_button.short_description = 'Actions'  # Set a description for the column
    inlines=[PrixSubstanceInlineAdmin]

    def add_view(self, request, form_url='', extra_context=None):
        # Your custom logic here to check URL parameters
        vente_id = request.GET.get('v', None)
        if not vente_id:
            message = "Vous devez specifier une vente"
            self.message_user(request, format_html(message), level='ERROR')
            referer = request.META.get('HTTP_REFERER', None)
            return redirect(referer or reverse('gesco:index'))
        return super().add_view(request, form_url, extra_context)

    def get_form(self, request, obj=None, **kwargs):
        # Customize the form based on GET parameters
        # form = super(FactureAdmin, self).get_form(request, obj, **kwargs)
        form = forms.FactureAdminForm
        # form = super().get_form(request, obj, **kwargs)

        # Check if it's an add action or a change action
        if obj is None:
            # Add action: prefill with request.GET.getlist('lingots')
            type_facture = request.GET.get('t', None)
            if not type_facture in [key for key, value in TYPES_FACTURE]:
                message = "Ce type de facture n'est pas defini!"
                self.message_user(request, format_html(message), level='ERROR')
                return form
            if form.base_fields.get('type_de_facture', None):
                form.base_fields['type_de_facture'].initial = type_facture
                form.base_fields['type_de_facture'].disabled = True

            vente_id = request.GET.get('v', None)
            try:
                vente = Vente.objects.get(id=vente_id)
                # initial_lingots = Lingot.objects.filter(pk__in=lingot_ids)
                form.base_fields['vente'].initial = vente
                form.base_fields['vente'].disabled = True
            except:
                message = "La vente correspondante n'existe pas!"
                self.message_user(request, format_html(message), level='ERROR')
                return form

        return form

    def save_model(self, request, obj, form, change):
        # Save the MouvementLingot model
        if not form.is_valid():
            self.message_user(request, "L'opération a échoué. Certains données sont invalides!")
            return

        if not change and not obj.user:  # Check if the object is being created (not updated)
            obj.user = request.user

        super(FactureAdmin, self).save_model(request, obj, form, change)

        if (not obj.vente or not obj.vente.vendre_selon) :
            self.message_user(request, f"Vous n'avez pas definie la vente et/ou le type de control selon lequel enregistrer la facture")
            return
        # Recolter les informations de poids de tous les lingots
        controllingots_vente = ControlLingot.objects.filter(
            control__vente=obj.vente,
            type_de_control=obj.vente.vendre_selon
        ).distinct('id')

        # Agreger les informations de poids venant des lingots selon le type de substance
        type_substances = {}
        for control_lingot in controllingots_vente:
            ps = PourcentageSubstanceControlLingot.objects.filter(control_lingot=control_lingot)
            for p in ps:
                key = str(p.type_de_substance.pk)
                poids = float(control_lingot.poids_brut*p.pourcentage/100)
                if type_substances.get(key, None):
                    type_substances[key] +=  poids
                else:
                    type_substances[key] = poids

        # Suprimer tous les prix pour les type de susbstances qui n'existent plus
        substance_ids = [int(k) for k in list(type_substances.keys())]
        obj.prixdessubstances_set.exclude(
            type_de_substance_id__in=substance_ids
        ).delete()

        # Mettre a jour les informations de pris pour chaque type de susbtance
        for mkey, value in type_substances.items():
            t_substance = TypeSubstance.objects.get(pk=mkey)
            print("mkey:::", mkey)
            print("TypeSubstance.objects.get(pk=mkey):::", t_substance)
            print("obj::: ", obj)
            p_substance = PrixDesSubstances.objects.filter(facture=obj,type_de_substance=t_substance).first()
            # print(f'mkey: {mkey} value: {value} t_substance: {t_substance} p_substance{p_substance}')
            # si le prix de substance existe pour ce type de dubstance: simple mise a jour

            if p_substance:
                # print(f'saving::: p_substance.id: {p_substance.pk} float(value): {float(value)} poids*float(obj.cours_du_dollar: {poids*float(obj.cours_du_dollar)}')
                # else:
                #     prix_substance = poids * float(p_substance.cours_de_substance)
                p_substance.poids = Decimal(value)
                p_substance.save()
            # sinon create l'objet prix pour cette substance pour la facture
            else:
                PrixDesSubstances.objects.create(
                    type_de_substance=TypeSubstance.objects.get(pk=mkey),
                    facture=obj,
                    poids=Decimal(value),
                ).save()
        

    # def get_readonly_fields(self, request, obj=None):
    #     read_only_fields = super().get_readonly_fields(request, obj)
    #     if obj and obj.facture_signe:
    #         read_only_fields = [
    #             field.name for field in self.model._meta.get_fields() if field.name not in ['facture_signe', 'prixdessubstances', 'id']
    #             ]
    #     # Get all field names of the model
    #     return read_only_fields



    def response_add(self, request, obj, post_url_continue=None):
        # Check if the 'your_variable' is present in the request
        if request.GET.get('v', None) and request.GET.get('t', None):
            # If the variable is present, customize the redirect URL
            return HttpResponseRedirect(reverse('gesco:commercial_vente_changelist'))
        # If the variable is not present, use the default redirect URL
        return super().response_add(request, obj, post_url_continue)

class FactureProformaAdmin(FactureAdmin):
    change_form_template = 'admin/commercial/factureproforma/change_form.html'
    def save_model(self, request, obj, form, change):
        obj.type_de_facture = "proforma"
        super(FactureProformaAdmin, self).save_model(request, obj, form, change)
        # Agreger les informations de poids venant des lingots selon le type de substance
        # type_substances = {}
        # for control_lingot in controllingots_vente:
        #     ps = PourcentageSubstanceControlLingot.objects.filter(control_lingot=control_lingot)
        #     for p in ps:
        #         key = str(p.type_de_substance.pk)
        #         poids = float(control_lingot.or_fin*p.pourcentage/100)
        #         if type_substances.get(key, None):
        #             type_substances[key] +=  poids
        #         else:
        #             type_substances[key] = poids

        # # Suprimer tous les prix pour les type de susbstances n'existent plus
        # substance_ids = [int(k) for k in list(type_substances.keys())]
        # PrixDesSubstances.objects.filter(
        #     facture=obj,
        #     type_de_prix=obj.type_de_facture
        # ).exclude(
        #     type_de_substance_id__in=substance_ids,
        # ).delete()

        # # Mettre a jour les informations de pris pour chaque
        # for mkey, value in type_substances.items():
        #     t_substance = TypeSubstance.objects.get(pk=mkey)
        #     p_substance = PrixDesSubstances.objects.filter(facture=obj,type_de_substance=t_substance, type_de_prix=obj.type_de_facture).first()
        #     # print(f'mkey: {mkey} value: {value} t_substance: {t_substance} p_substance{p_substance}')
        #     # si le prix de substance existe pour ce type de dubstance: simple mise a jour
        #     if p_substance:
        #         # print(f'saving::: p_substance.id: {p_substance.pk} float(value): {float(value)} poids*float(obj.cours_du_dollar: {poids*float(obj.cours_du_dollar)}')
        #         p_substance.poids = float(value)
        #         p_substance.prix = poids*float(obj.cours_du_dollar)
        #         p_substance.save(update_fields=['poids', 'prix'])
        #     # sinon create l'objet prix pour cette substance pour la facture
        #     else:
        #         PrixDesSubstances.objects.create(
        #             type_de_substance=TypeSubstance.objects.get(pk=mkey),
        #             facture=obj,
        #             type_de_prix='proforma',
        #             poids=value,
        #         ).save()
        # # Save the MouvementLingot model
        # if not form.is_valid():
        #     self.message_user(request, "L'opération a échoué. Certains données sont invalides!")
        #     return

        # if not change and not obj.user:  # Check if the object is being created (not updated)
        #     obj.user = request.user

        # # S'assurer qu'il existe des control pour cette vente ou puisser les informations de poids
        # controls_vente = Control.objects.filter(vente=obj.vente, type_de_control=obj.poids_selon)
        # if len(controls_vente) == 1:
        #         if len(controls_vente) == 0:
        #             self.message_user(request, "Vous avez choisi {} comme source de poids sans en avoir fait ce type de control au prealable.")
        #             return
        # obj.save()
        # if obj.vente:
        #     #Verifier que le poids selon le quelle on veut faire la facture existe
        #     lingots_vente = Lingot.objects.filter(vente=obj.vente, controllingot__isnull=True)
        #     for lingot in lingots_vente:
        #         control_lingot = ControlLingot.objects.create(
        #             lingot=lingot,
        #             control=obj,
        #             user=request.user,
        #         )
        #         if obj.type_control:
        #             control_lingot.type_control = obj.type_control
        #         control_lingot.save()

class FactureDefinitiveAdmin(FactureAdmin):
    change_form_template = 'admin/commercial/facturedefinitive/change_form.html'
    def save_model(self, request, obj, form, change):
        obj.type_de_facture = "definitive"
        print("obj.type_de_facture::", obj.type_de_facture)
        super(FactureDefinitiveAdmin, self).save_model(request, obj, form, change)

class TypeSubstanceAdmin(admin.ModelAdmin):
    list_display = ['libelle', 'symbole', 'description']


class ClientAdmin(admin.ModelAdmin):
    # form = forms.VenteAdminForm
    model = Client
    list_display = ['societe', 'email', 'telephone', 'type_de_client', 'pays', 'reference_societe', 'envoyer_sms']
    exclude = [

    ]
    show_change_link = True
    fields = ['societe', 'reference_societe', 'nom', 'type_de_client', 'addresse', 'email', 'telephone', 'pays', 'document_identite', 'reference_document_identite', 'autre_document', 'description']
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3})},
    }

    def envoyer_sms(self, obj):
        url = reverse('gesco:commercial_smsclient_add')
        return format_html('<a class="button default" href="{}?c={}">ENVOYER SMS</a>', url, obj.id)

    def envoie_message(self, request, queryset):

         # Create a list of primary keys of the selected ModelB instances
        user_ids = '&c='.join(map(str, queryset.values_list('pk', flat=True)))

        # Redirect to the add form for ModelA with the initial values
        add_sms_url = reverse('gesco:commercial_smsclient_add') + f'?c={user_ids}'
        return HttpResponseRedirect(add_sms_url)

    actions = ['envoie_message']
    envoie_message.short_description = "Envoyer un message a la selection"

class SMSAdmin(admin.ModelAdmin):
    form = forms.SMSAdminForm
    model = SMS
    list_display = ['__str__', 'message', 'etat', 'resend']
    exclude = [
        'type_de_message',
        'envoye'
    ]
    readonly_fields = ['list_non_envoye']
    show_change_link = True

    def etat(self, obj):
        text_content = 'Succes'
        style = "background-color: #44b78b; padding: 5px; border-radius: 5px; color: white;"
        if not obj.envoye or not obj.list_non_envoye is None or not str(obj.list_non_envoye) == '':
            # print(f"obj.list_non_envoye::: {obj}", f"|{obj.list_non_envoye}|")
            text_content = 'Partiel'
            style = "background-color: #f9cc1c; padding: 5px; border-radius: 5px; color: white"
        return format_html(
                f'<span style="{style}">{text_content}</span>'
            )
    def resend(self, obj):
        if obj.list_non_envoye is not None:
            if not obj.envoye or not obj.list_non_envoye is None or not str(obj.list_non_envoye) == '':
                if obj.type_de_message == 'f':
                    model_name = 'smsfournisseur'
                elif obj.type_de_message == 'c':
                    model_name = 'smsclient'
                else:
                    model_name = 'sms'

                url_resend = reverse(f'gesco:commercial_{model_name}_change', args=[obj.pk])
                return format_html(
                        f'<a class="button" href="{url_resend}">Renvoyer aux echecs</div>'
                    )
        else:
            return ''

    def get_form(self, request, obj=None, **kwargs):
        # Customize the form based on GET parameters
        form = super(SMSAdmin, self).get_form(request, obj, **kwargs)
        # form = super().get_form(request, obj, **kwargs)
        # Check if it's an add action or a change action
        if obj is None:
            if 'f' in request.GET:
                f = request.GET.getlist('f', [])
                if len(f) > 0:
                    fournisseurs = Fournisseur.objects.filter(id__in=[int(i) for i in f])
                    fournisseurs_without_tels = fournisseurs.filter(telephone__isnull=True).distinct('id')
                    if len(fournisseurs_without_tels) > 0:
                        message = ""
                        for f in fournisseurs_without_tels:
                            url = reverse('gesco:commercial_fournisseur_change', args=[f.pk])
                            message += f'<br><a href="{url}">{f}</a>'
                        self.message_user(request, format_html("Le numero de telephone n'est pas renseingé pour ces clients:" + message), level="WARNING")
                    if form.base_fields.get('fournisseurs', None):
                        form.base_fields['fournisseurs'].initial = fournisseurs
                    tels = fournisseurs.values_list('telephone', flat=True)
                    print('tels', list(tels))

            elif 'c' in request.GET:
                c = request.GET.getlist('c', [])
                if len(c) > 0:
                    clients = Client.objects.filter(id__in=[int(i) for i in c])
                    clients_without_tels = clients.filter(telephone__isnull=True)
                    if len(clients_without_tels) > 0:
                        message = ""
                        for c in clients_without_tels:
                            url = reverse('gesco:commercial_client_change', args=[c.pk])
                            message += f'<br><a href="{url}">{c}</a>'
                        self.message_user(request, format_html("Le numero de telephone n'est pas renseingé pour ces clients:" + message), level="WARNING")
                    
                    tels = clients.values_list('telephone', flat=True)
                    if form.base_fields.get('clients', None):
                        form.base_fields['clients'].initial = clients
                    print('tels', list(tels))
        return form

    def save_model(self, request, obj, form, change):
        super(SMSAdmin, self).save_model(request, obj, form, change)
        print("obj.type_de_message", obj.type_de_message)
        # Check if 'envoye' is False
        obj.save()
        if not obj.envoye:
            # Determine the type of message (client or fournisseur)
            if obj.type_de_message == 'c':
                # Retrieve telephone numbers for clients
                clients = form.cleaned_data['clients']
                telephone_numbers = set([client.telephone for client in clients])
            elif obj.type_de_message == 'f':
                # Retrieve telephone numbers for fournisseurs
                fournisseurs = form.cleaned_data['fournisseurs']
                print('fournisseurs = obj.fournisseurs.all():::', obj.fournisseurs)
                print('fournisseurs:::', fournisseurs)
                telephone_numbers = [fournisseur.telephone for fournisseur in fournisseurs]
                print("telephone_numbers in f:::", telephone_numbers)
            else:
                telephone_numbers = []
            print("telephone_numbers", telephone_numbers)
            # Filter out the succeeded numbers
            try:
                succeeded_numbers = envoyer_message(obj.message, *telephone_numbers)
            except:
                pass

            # Find non-succeeded numbers
            print('set(telephone_numbers)::', set(telephone_numbers))
            print('set(succeeded_numbers)', set(succeeded_numbers))
            non_succeeded_numbers = set(telephone_numbers) - set(succeeded_numbers)
            # Update the 'list_non_envoye' field
            print("telephone_numbers::non_succeeded_numbers", non_succeeded_numbers)
            non_succeeded_numbers.discard(None)
            print("telephone_numbers::non_succeeded_numbers after", non_succeeded_numbers)
            if non_succeeded_numbers is not None and len(non_succeeded_numbers) > 0:
                print('first_case')
                obj.list_non_envoye = ';'.join(non_succeeded_numbers)
            else:
                print('second_case')
                obj.list_non_envoye = ''

            # Mark the message as 'envoye'
            obj.envoye = True

            # Save the updated SMS object
            obj.save()

        # Check if 'list_non_envoye' is not empty
        elif obj.list_non_envoye:
            # Split the list_non_envoye string and get a list of numbers
            non_envoye_numbers = obj.list_non_envoye.split(';')
            print("non_succeeded_numbers", non_envoye_numbers)

            # Filter out the succeeded numbers
            try:
                succeeded_numbers = envoyer_message(obj.message, *non_envoye_numbers)
            except:
                pass
            print("succeeded_numbers", succeeded_numbers)

            # Find non-succeeded numbers
            non_succeeded_numbers = set(non_envoye_numbers) - set(succeeded_numbers)

            # Update the 'list_non_envoye' field
            obj.list_non_envoye = ';'.join(non_succeeded_numbers)

            # Save the updated SMS object
            obj.save()


class SMSClientAdmin(SMSAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super(SMSClientAdmin, self).get_form(request, obj, **kwargs)
        if form.base_fields.get('fournisseurs', None):
            form.base_fields.pop('fournisseurs')
        return form
    
    def save_model(self, request, obj, form, change):
        obj.type_de_message = "c"
        super(SMSClientAdmin, self).save_model(request, obj, form, change)


class SMSFournisseurAdmin(SMSAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super(SMSFournisseurAdmin, self).get_form(request, obj, **kwargs)
        if form.base_fields.get('clients', None):
            form.base_fields.pop('clients')
        return form

    def save_model(self, request, obj, form, change):
        obj.type_de_message = "f"
        super(SMSFournisseurAdmin, self).save_model(request, obj, form, change)

class EmplacementLingotAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'pays', 'type_emplacement']
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3})},
        # Add more overrides as needed
    }

class MouvementLingotLingotInline(admin.TabularInline):
    model = MouvementLingotLingot
    extra = 1  # Number of empty forms to display
    readonly_fields = ['lingot']

class MouvementLingotAdmin(admin.ModelAdmin):

    form = forms.MouvementLingotAdminForm
    # inlines = [MouvementLingotLingotInline]
    list_display = ['numero_mouvement', 'destination', 'date_deplacement', 'user', 'etat']
    exclude = ['created']
    from django.contrib.admin import DateFieldListFilter
    from rangefilter.filter import DateRangeFilter
    list_filter = ['mouvementlingotlingot__lingot_id', 'destination', ('date_deplacement', DateFieldListFilter), ('date_deplacement', DateRangeFilter)]
    date_hierarchy = 'date_deplacement'

    def get_form(self, request, obj=None, **kwargs):
        # Customize the form based on GET parameters
        form = super(MouvementLingotAdmin, self).get_form(request, obj, **kwargs)
        # form = super().get_form(request, obj, **kwargs)

        # Check if it's an add action or a change action
        if obj is None:
            # Add action: prefill with request.GET.getlist('lingots')
            lingot_ids = request.GET.getlist('l', [])
            initial_lingots = Lingot.objects.filter(pk__in=lingot_ids)
            form.base_fields['lingots_a_deplacer'].initial = initial_lingots

            print('request.GET : ', request.GET)
            print('lingot_ids : ', lingot_ids)


    #     # Check if a parameter is present in the request
    #     if 'ft' in request.GET:
    #         fonte_id = request.GET['ft']
    #         kwargs['form'] = forms.LingotAdminForm
    #         # Remove the specified field from the form

        return form


    def save_model(self, request, obj, form, change):
        # Save the MouvementLingot model
        if not form.is_valid():
            self.message_user(request, "L'opération a échoué. Erreur interne!")
            return

        if not change and not obj.user:  # Check if the object is being created (not updated)
            obj.user = request.user


        # Save the MouvementLingot instance

        # Retrieve Lingot objects based on provided IDs
        lingot_ids = form.cleaned_data['lingots_a_deplacer'].all()
        selected_lingots = Lingot.objects.filter(id__in=lingot_ids)

        # Associate selected Lingots with the MouvementLingot instance
        print('obj before: ', obj)
        obj.save()
        print('obj: ', obj)
        obj.lingots.set(selected_lingots)
        updated = MouvementLingotLingot.objects.exclude(
                mouvement_lingot=obj.pk
            ).filter(
                lingot_id__in=obj.lingots.values_list('id', flat=True)
            ).update(moved=True)
        print('updated: ', updated)

        print('lingots ids in form: ', lingot_ids)
        print('selected lingots:', selected_lingots)
        print('cleaned lingot:', form.cleaned_data['lingots_a_deplacer'])
        print('saved lingot:', obj.lingots.all())

    def response_add(self, request, obj, post_url_continue=None):
        # Check if the 'your_variable' is present in the request
        return HttpResponseRedirect(reverse('gesco:commercial_transferedlingot_changelist'))
