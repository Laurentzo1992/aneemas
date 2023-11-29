from django.contrib import admin
from django.forms import CharField, DecimalField, Textarea, ValidationError
from django.http import Http404, HttpResponseRedirect
from django.db import IntegrityError, models, transaction
from django.shortcuts import render

from authentication.models import User
from commercial.views import commercial_payement_archiver_view, commercial_tarification_transferer
from .models import (
    ControlBUMIGEB,
    Fournisseur, 
    DirectionLingot, 
    EmplacementLingot, 
    Factures, Fichecontrol, 
    Fonte, Lingot,
    LingotFondus, 
    ModePayement, 
    MouvementLingot, 
    Pesee, 
    FicheTarification,
    PieceJointe, 
    StragieTarification,
    TransferedFicheTarification,
    TransferedFicheTarificationManager, 
    TypeFournisseur, 
    TypeSubstance
    )
from django.urls import path, reverse
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
    model = Fichecontrol
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
        print('obj.etat:: ', obj.etat)
        url = reverse('gesco:commercial_lingot_change', args=[14])
        print('format:: ')
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
    list_display = ['numero', 'date_sortie', 'date_retour', 'user', 'etat', 'custom_actions']
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
    
    def custom_actions(self, obj):
        class_name = 'disabled-link' if self.is_etat_in_filter else ''
        fondre_url = reverse('gesco:commercial_lingot_change', args=[obj.id])
        return format_html('<a class="button default {}" href="{}?ft={}">Reintegrer</a>', class_name, fondre_url, obj.id)

class FichecontrolAdmin(admin.ModelAdmin):
    form = forms.FicheControlAdminForm
    inlines = [LingotInLineAdmin]
    # inlines = [LingotTabularInLineAdmin]
    list_display = ['numero', 'user', 'fournisseur', 'date_control', 'modified', 'custom_action_button']
    exclude = ['user']
    list_filter = ['numero', 'user', 'fournisseur', 'lingot']

    def custom_action_button(self, obj):
        generate_pdf_url = reverse('generate-fiche-control', args=[obj.pk])  # Replace 'generate_pdf' with your actual URL name
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

    def get_queryset(self, request):
        # Get the original queryset
        queryset = super().get_queryset(request)

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
        return form

class FicheTarificationAdmin(admin.ModelAdmin):
    form = forms.FicheTarificationAdminForm
    change_form_template = 'commercial/admin/fichecontrol/add.html'
    list_display = ['numero', 'fichecontrol', 'user', 'date_tarification', 'modified', 'custom_action_button']
    exclude = ['user', 'transferer', 'archived']
    list_filter = ['numero', 'user', 'fichecontrol']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<path:object_id>/transferer/', self.admin_site.admin_view(commercial_tarification_transferer), name='commercial_tarification_transferer'),
        ]
        return custom_urls + urls

    def save_model(self, request, obj, form, change):
        # Save the Payment model
        super().save_model(request, obj, form, change)

        if not change and not obj.user:  # Check if the object is being created (not updated)
            obj.user = request.user

        fichecontrol_id = request.GET.get('a')
        # Check if the related object exists
        try:
            fichecontrol = Fichecontrol.objects.get(id=fichecontrol_id)
            obj.fichecontrol = fichecontrol
        except TransferedFicheTarification.DoesNotExist:
            raise Http404(f"La fiche de control correspondante n'existe pas!")
        
        super().save_model(request, obj, form, change)

    def custom_action_button(self, obj):
        transferer_url = reverse('gesco:commercial_tarification_transferer', args=[obj.id])
        generate_pdf_url = reverse('generate-fiche-control', args=[obj.pk])  # Replace 'generate_pdf' with your actual URL name
        return format_html(
            '<a class="button default" href="{}">Payement</a>'
            '<a class="button" href="{}">Archiver</a>'
            ' <a class="button print-button" href="{}" data-url={}>Imprimer</a>',
            transferer_url,
            generate_pdf_url,
            generate_pdf_url,
            generate_pdf_url,
        )
        
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

        
        fichecontrol_id = request.GET.get('a')
        # Check if the related object exists
        try:
            fichecontrol = Fichecontrol.objects.get(id=fichecontrol_id)
            form.fichecontrol = fichecontrol
        except TransferedFicheTarification.DoesNotExist:
            raise Http404(f"La fiche de control correspondante n'existe pas!")
        
        # Pass the initial data to the form
        initial_data = {
            'reference': '######',  # Set your initial data here
        }
        form.base_fields['fichecontrol'].initial = fichecontrol
        
        form.user = request.user
        return form
    

class FichePaiementAdmin(FicheTarificationAdmin):
    pass

class LingotAdmin(admin.ModelAdmin):
    # form = forms.LingotAdminForm
    inlines = [PeseeInLineAdmin]
    list_display = ['numero', 'fournisseur', 'user', 'fichecontrol', 'date_reception', 'modified', 'custom_action_button']
    exclude = ['user']
    readonly_fields = ['user', 'poids_brut', 'poids_immerge', 'ecart', 'densite', 'titre', 'or_fin']
    fields = ['date_reception', 'observation',  'poids_brut', 'poids_immerge', ('ecart', 'densite'), ('titre', 'or_fin')]
    list_filter = ['numero', 'fournisseur', 'fichecontrol', 'user', 'titre', IsMeltedFilter]

    def custom_action_button(self, obj):
        return format_html('<a class="button" href="#">Voir</a> <a class="button default" href="#">Imprimer</a>')
    custom_action_button.allow_tags = True
    custom_action_button.short_description = 'Actions'  # Set a description for the column
    
    actions = ['fondre', 'control_BUMIGEB']  # Add your custom action here

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3})},
    }

    
    def get_filters_params(self, request, *args, **kwargs):
        params = super().get_filters_params(request, *args, **kwargs)

        # Set a default value for the custom filter if it's not present in the request
        if 'is_melted' not in params:
            params['is_melted'] = 'no'
        print(params)
        return params

    def fondre(self, request, queryset):

        already_linked_items = queryset.filter(fonte__isnull=False)

        if already_linked_items.exists():
            # Display an error message for already linked items
            error_message = "Echec, les lingots suivants sont deja fondus:"
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

           
        
        

class FournisseurAdmin(admin.ModelAdmin):
    inlines = [FichecontrolInlineAdmin, LingotInLineAdmin]
    list_display = ['nom', 'prenom', 'email', 'telephone', 'type_fournisseur']
    exclude = []

    add_form_template = 'commercial/admin/fournisseur/add.html'

    def custom_action_button(self, obj):
        return format_html('<a class="button" href="#">Modifier</a> <a class="button default" href="#">Archiver</a>')
    custom_action_button.allow_tags = True
    custom_action_button.short_description = 'Actions'  # Set a description for the column
    
    actions = ['Archiver']  # Add your custom action here

    def tarifier(self, request, queryset):
        selected_ids = queryset.values_list('id', flat=True)

    tarifier.short_description = 'Archiver'

class PayementAdmin(admin.ModelAdmin):
    # form = forms.PayementAdminFrom
    list_display = ['__str__', 'user', 'fournisseur', 'montant', 'piecejointe', 'custom_actions']
    fields = ['montant', 'reference', 'piecejointe']
    exclude = ['direction', 'archived', 'actif', 'confirmed', 'fichetarification']
    readonly_fields = ['user', 'fournisseur', ]

    def fournisseur(self, obj):
        return 0
    

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        
        
        # Pass the initial data to the form
        initial_data = {
            'reference': '######',  # Set your initial data here
        }
        form.base_fields['reference'].initial = initial_data.get('reference', None)
        form.user = request.user
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
        
        return format_html('<a class="button default {}" href="{}">Archiver</a>', class_name, url)
    
    custom_actions.allow_tags = True
    
    def save_model(self, request, obj, form, change):
        # Save the Payment model
        super().save_model(request, obj, form, change)

        if not change and not obj.user:  # Check if the object is being created (not updated)
            obj.user = request.user

        fichetarification_id = request.GET.get('a')
        # Check if the related object exists
        try:
            fichetarification = TransferedFicheTarification.objects.get(id=fichetarification_id)
            obj.fournisseur = fichetarification.fichecontrol.fournisseur
        except TransferedFicheTarification.DoesNotExist:
            raise Http404(f"La fiche de tarification correspondante n'existe pas!")
        
        
        obj.fichetarification = fichetarification
        
        super().save_model(request, obj, form, change)

class TransferedFicheTarificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'fournisseur', 'numero', 'fichecontrol', 'montant', 'resteapayer', 'custom_action_button']  # Add your actual fields here

    def custom_action_button(self, obj):
        url = reverse('gesco:commercial_payement_add')
        return format_html('<a class="button default" href="{}?a={}">Payer</a>', url, obj.id)
        # return format_html('<a class="button default" href="#">Payer</a>')
    
    def montant(self, obj):
        return 0
    
    def resteapayer(self, obj):
        return 0

    def fournisseur(self, obj):
        return obj.fichecontrol.fournisseur
    
    actions = ["renvoyer_en_tarification"]

    def renvoyer_en_tarification(self, request, queryset):
        queryset.update(transferer=False)
    
        self.message_user(request, f'Les fiches ont étées renvoyé en tarification avec succès!')
    
    renvoyer_en_tarification.short_description = "Renvoyer la selection en tarification"


    montant.shord_description = 'Total a payer'
    resteapayer.shord_description = 'Reste a payer'
    custom_action_button.allow_tags = True
    custom_action_button.short_description = 'Actions'  # Set a description for the column
    