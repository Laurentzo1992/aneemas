
from asyncio import format_helpers
from types import NoneType
from typing import Any
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field
from django.urls import reverse

from commercial.querysets import stock_queryset
from .models import *
from django.forms.models import inlineformset_factory
from django.contrib import admin
from .models import PieceJointe, Fichecontrol


from .models import Lingot, Fonte
from django.contrib.admin.widgets import FilteredSelectMultiple, RelatedFieldWidgetWrapper
from django.utils.html import format_html

# class SortieFonteAdminForm(forms.ModelForm):
#     class Meta:
#         model = Fonte
#         fields = ['lingots', 'date_sortie']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         # Filter the queryset for the 'books' field based on your criteria
#         # self.fields['lingots'].queryset = Lingot.objects.filter(fonte__isnull=True)

#         if self.instance.pk:
#             # Retrieve and add the lingots associated with this Fichecontrol
#             print(self.base_fields)
#             print(self.fields)
            # self.fields['lingots'].queryset = self.fields['lingots'].initial

# class RetourFonteAdminForm(forms.ModelForm):

#     # poids_brut = forms.DecimalField(max_digits=10, decimal_places=4)
#     # poids_immerge = forms.DecimalField(max_digits=10, decimal_places=4)
#     class Meta:
#         model = Fonte
#         exclude = ['created']

#     # def formfield_for_dbfield(self, db_field, request, **kwargs):
#     #     # Customize the form field for the virtual fields
#     #     if db_field.name in ['poids_brut', 'poids_immerge']:
#     #         return db_field.formfield(**kwargs)
#     #     return super().formfield_for_dbfield(db_field, request, **kwargs)



    # def __init__(self, *args, **kwargs):
    #     super(RetourFonteAdminForm, self).__init__(*args, **kwargs)
        # self.fields['lingots'].widget.attrs['readonly'] = True
        # self.base_fields['date_sortie'].widget.attrs['readonly'] = True


        # self.fields['lingots'].disabled = True
        # self.fields['date_sortie'].disabled = True
        # self.fields['date_retour'].required = True



class FicheTarificationAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FicheTarificationAdminForm, self).__init__(*args, **kwargs)
        self.fields['fichecontrol'].widget.attrs['readonly'] = True
        self.fields['numero'].widget.attrs['readonly'] = True
        # self.fields['fichecontrol'].widget = forms.HiddenInput()
        self.fields['fichecontrol'].disabled = True
        self.fields['numero'].disabled = True
        

        if self.fields.get('representantfournisseur', None):
            self.fields['representantfournisseur'].queryset = self.instance.representant_fournisseur_set.all()
        
        if not self.instance.pk and self.fields.get('marge', None):
            self.fields['marge'].initial = 5

    def clean(self) -> dict[str, Any]:
        return super().clean()
        attachment_validation_logic(self, 'document_signe')
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "fichecontrol":  # Replace with the actual field name
            kwargs["queryset"] = Fichecontrol.objects.all()  # Define your filter criteria here
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    
    def save(self, commit=False, *args, **kwargs):
        instance = super(FicheTarificationAdminForm, self).save(commit=False)
        # Save the instance if it's not yet saved
        if not instance.pk:
            instance.save()

        if self.user and not self.instance.user:
                instance.user = self.user
        if commit:
            instance.save()

        return instance

from django.contrib.admin import AdminSite

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
        urls = super().get_urls()
        custom_urls = []

        return urls + custom_urls


class CustomRelatedFieldWidgetWrapper(RelatedFieldWidgetWrapper):
    def get_related_url(self, info, action, *args):
        # Customize the URL for related field lookup if needed
        return super().get_related_url(info, action, *args)

from django.db import models

class CustomRemoteField(models.Field):
    def __init__(self, *args, **kwargs):
        kwargs['editable'] = False
        kwargs['null'] = True
        kwargs['blank'] = True
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs['editable']
        del kwargs['null']
        del kwargs['blank']
        del kwargs['related_name']
        return name, path, args, kwargs

    def get_internal_type(self):
        return 'ForeignKey'

    def get_db_prep_save(self, *args, **kwargs):
        return None

class FonteAdminForm(forms.ModelForm):
    lingots = forms.ModelMultipleChoiceField(
        queryset=Lingot.objects.filter(fonte__isnull=True),
        required=False,
        help_text="Maintenez la touche 'Ctrl', ou 'Command' sur un Mac, enfoncée pour en sélectionner plusieurs."
    )

    class Meta:
        model = Fonte
        fields = ['lingots', 'observation']

    def __init__(self, *args, **kwargs):
        super(FonteAdminForm, self).__init__(*args, **kwargs)

        self.fields['lingots'].widget = RelatedFieldWidgetWrapper(
            self.fields['lingots'].widget,
            Pesee._meta.get_field('lingot').remote_field,
            CommercialAdmin(name='gesco'),
            can_delete_related=True,
            can_add_related=True,
            can_change_related=True,
        )

        if self.instance.pk:
            # Retrieve and add the lingots associated with this Fichecontrol
            self.fields['lingots'].initial = Lingot.objects.filter(fonte=self.instance)
            self.fields['lingots'].queryset = self.fields['lingots'].queryset | self.fields['lingots'].initial

    def clean(self):
        cleaned_data = super().clean()
        if self.instance.pk:
            selected_lingots = cleaned_data.get('lingots')
            if selected_lingots:
                existing_fontes = Lingot.objects.filter(
                    id__in=selected_lingots.values_list('id', flat=True),
                    fonte__isnull=False
                ).exclude(fonte=self.instance).values_list('fonte__id', flat=True).distinct()
                if len(existing_fontes) >= 1:
                    raise forms.ValidationError(
                        'Au moins un des lingots selectionnés est deja associé à une fiche de control differente.'
                    )

        return cleaned_data

    def save(self, commit=False, *args, **kwargs):
        instance = super(FonteAdminForm, self).save(commit=False)

        # Save the instance if it's not yet saved
        if not instance.pk:
            instance.save()
        else:
            self.fields['lingots'].initial.update(fonte=None)

        # if self.user and not instance.user:
        #     instance.user = self.user
        if commit:
            instance.save()

        # Disassociate lingots from this Fichecontrol
        Lingot.objects.filter(fonte=instance).update(fonte=None)

        # Associate selected lingots with this Fichecontrol
        selected_lingots = self.cleaned_data.get('lingots')
        if selected_lingots is not None:
            selected_lingots.update(fonte=instance)

        return instance

class ControlBUMIGEBAdminForm(forms.ModelForm):
    lingots = forms.ModelMultipleChoiceField(
        queryset=Lingot.objects.filter(control_bumigeb__isnull=True),
        required=False,
        help_text="Maintenez la touche 'Ctrl', ou 'Command' sur un Mac, enfoncée pour en sélectionner plusieurs."
    )

    class Meta:
        model = ControlBUMIGEB
        fields = ['numero_lot', 'lingots', 'observation', 'date_retour']

    def __init__(self, *args, **kwargs):
        super(ControlBUMIGEBAdminForm, self).__init__(*args, **kwargs)
        self.fields['numero_lot'].widget.attrs['disabled'] = True
        self.fields['numero_lot'].widget.attrs['readonly'] = True
        self.fields['lingots'].widget = RelatedFieldWidgetWrapper(
            self.fields['lingots'].widget,
            Pesee._meta.get_field('lingot').remote_field,
            CommercialAdmin(name='gesco'),
            can_delete_related=True,
            can_add_related=True,
            can_change_related=True,
        )

        if self.instance.pk:
            # Retrieve and add the lingots associated with this Fichecontrol
            self.fields['lingots'].initial = Lingot.objects.filter(control_bumigeb=self.instance)
            self.fields['lingots'].queryset = self.fields['lingots'].queryset | self.fields['lingots'].initial

    def clean(self):
        cleaned_data = super().clean()

        if self.instance.pk:
            selected_lingots = cleaned_data.get('lingots')
            if selected_lingots:
                existing_control_bumigebs = Lingot.objects.filter(
                    id__in=selected_lingots.values_list('id', flat=True),
                    control_bumigeb__isnull=False
                ).exclude(control_bumigeb=self.instance).values_list('control_bumigeb__id', flat=True).distinct()
                if len(existing_control_bumigebs) >= 1:
                    raise forms.ValidationError(
                        'Au moins un des lingots selectionnés est deja associé à une fiche de control differente.'
                    )

        return cleaned_data

    def save(self, commit=False, *args, **kwargs):
        instance = super(ControlBUMIGEBAdminForm, self).save(commit=False)

        # Save the instance if it's not yet saved
        if not instance.pk:
            instance.save()
        else:
            self.fields['lingots'].initial.update(control_bumigeb=None)

        # if self.user and not instance.user:
        #     instance.user = self.user
        if commit:
            instance.save()

        # Disassociate lingots from this Fichecontrol
        Lingot.objects.filter(control_bumigeb=instance).update(control_bumigeb=None)

        # Associate selected lingots with this Fichecontrol
        selected_lingots = self.cleaned_data.get('lingots')
        if selected_lingots is not None:
            selected_lingots.update(control_bumigeb=instance)

        return instance

class FicheControlAdminForm(forms.ModelForm):
    lingots = forms.ModelMultipleChoiceField(
        queryset=stock_queryset().exclude(fichecontrol__isnull=False),
        required=False,
        help_text="Maintenez la touche 'Ctrl', ou 'Command' sur un Mac, enfoncée pour en sélectionner plusieurs."
    )

    class Meta:
        model = Fichecontrol
        exclude = ['user', 'archived']
        fields = ['fournisseur', 'date_control', 'lingots', 'observation', 'document_signe', 'numero']

    def __init__(self, *args, **kwargs):
        super(FicheControlAdminForm, self).__init__(*args, **kwargs)
        self.fields['lingots'].widget = RelatedFieldWidgetWrapper(
            self.fields['lingots'].widget,
            Pesee._meta.get_field('lingot').remote_field,
            CommercialAdmin(name='gesco'),
            can_delete_related=True,
            can_add_related=True,
            can_change_related=True,
        )

        if self.instance.pk:
            # Retrieve and add the lingots associated with this Fichecontrol
            if self.fields.get('lingots', None):
                self.fields['lingots'].initial = self.instance.lingot_set.all()
                self.fields['lingots'].queryset = self.fields['lingots'].queryset | self.fields['lingots'].initial
            
    def clean(self):
        cleaned_data = super().clean()
        attachment_validation_logic(self, 'document_signe')
        selected_lingots = cleaned_data.get('lingots')
        fournisseur = cleaned_data.get('fournisseur', None)
        if any(l.fournisseur != fournisseur for l in selected_lingots):
            errors = [f"Les lingots suivants n'appartiennent pas au fournisseur: {fournisseur}"]
            errors += [f"{l}" for l in selected_lingots.exclude(fournisseur=fournisseur)]
            raise ValidationError(errors)
        if len(list(set(selected_lingots.distinct().values_list('fournisseur__id', flat=True)))) > 1:
                self.add_error('lingots', 'Une fiche de control doit contenir des lingots appartenant au meme fournisseur.')

        if len(selected_lingots) >= 1:
            linked_fichecontrols = selected_lingots.filter(fichecontrol__isnull=False)

            if  len(linked_fichecontrols) != 0 and self.instance.pk:
                linked_fichecontrols = linked_fichecontrols.exclude(fichecontrol=self.instance)

            print("linked_fichecontrols", linked_fichecontrols)
            if len(linked_fichecontrols.distinct())  >= 1:
                self.add_error('lingots', 'Au moins un des lingots selectionnés est deja associé à une fiche de control differente.')

        return cleaned_data

    def save(self, commit=False, *args, **kwargs):
        instance = super(FicheControlAdminForm, self).save(commit=False)

        # Save the instance if it's not yet saved
        if not instance.pk:
            instance.save()
        elif self.fields['lingots'].initial:
            self.fields['lingots'].initial.update(fichecontrol=None)

        if self.user and not self.instance.user:
            instance.user = self.user
        if commit:
            instance.save()

        # Disassociate lingots from this Fichecontrol
        Lingot.objects.filter(fichecontrol=instance).update(fichecontrol=None)

        # Associate selected lingots with this Fichecontrol
        selected_lingots = self.cleaned_data.get('lingots')
        if selected_lingots is not None:
            selected_lingots.update(fichecontrol=instance)

        return instance

class FicheControlAdminForm2(forms.ModelForm):
    lingots = forms.ModelMultipleChoiceField(
        queryset=Lingot.objects.filter(fichecontrol__isnull=True), # Lingots libres
        required=False,
        help_text = "Maintenez la touche 'Ctrl', ou 'Command' sur un Mac, enfoncée pour en sélectionner plusieurs.",
    )


    def can_add_related():
        return True

    class Meta:
        model = Fichecontrol
        fields = ['fournisseur', 'date_control', 'lingots', 'observation']


    def __init__(self, *args, **kwargs):
        super(FicheControlAdminForm, self).__init__(*args, **kwargs)

        if self.instance.pk:
            # Si l'instance de Fichecontrol existe déjà, recuperer ajouter ses lingots
            self.fields['lingots'].initial = self.fields['lingots'].queryset | self.instance.lingot_set.all()

    def clean(self):
        # Gerer le cas ou on voudrait joindre des lingots deja lié a un autre fiche de control
        cleaned_data = super().clean()
        if self.instance.pk:
            selected_lingots = cleaned_data.get('lingots')
            if selected_lingots:
                existing_fichecontrols = Lingot.objects.filter(
                    id__in=selected_lingots.values_list('id', flat=True),
                    fichecontrol__isnull=False
                ).values_list('fichecontrol__id', flat=True).distinct()

            if not len(existing_fichecontrols) == 1:
                raise forms.ValidationError('Votre selection de lingots contient un(ou des) lingots dejà lié(s) à un(ou des) fiche(s) de control(s).')
            

        return cleaned_data

    # def save(self, *args, **kwargs):
    #     # FIXME: 'commit' argument is not handled
    #     # TODO: Wrap reassignments into transaction
    #     # NOTE: Previously assigned Foos are silently reset
    #     instance = super(FicheControlAdminForm, self).save(commit=False)
    #     self.fields['lingots'].initial.update(fichecontrol=None)
    #     self.cleaned_data['lingots'].update(fichecontrol=instance)
    #     return instance
    def save(self, *args, **kwargs):
        instance = super(FicheControlAdminForm, self).save(commit=False)


        # Make sure self.cleaned_data['lingots'] is not None
        selected_lingots = self.cleaned_data.get('lingots')
        if selected_lingots is not None:
            # Update the fichecontrol for selected lingots
            selected_lingots.update(fichecontrol=instance)

        return instance


class LingotAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LingotAdminForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Lingot
        exclude = ['user']

    def clean(self):
        cleaned_data = super().clean()
        
        
class PeseeForm(forms.ModelForm):
    class Meta:
        model = Pesee
        fields = ['poids_brut', 'poids_immerge', 'date_pesee', 'observation']

    def __init__(self, *args, **kwargs):
        super(PeseeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('poids_brut', css_class='form-control'),
            Field('poids_immerge', css_class='form-control'),
            Field('date_pesee', css_class='form-control'),
            Field('observation', css_class='form-control'),
        )

class FichecontrolLingotInlineFormset(forms.BaseInlineFormSet):
    def add_fields(self, form, index):
        super().add_fields(form, index)
        lingot = form.instance.lingot  # Get the Lingot associated with this through model

        # Add fields from Lingot model to the form
        form.fields['numero'] = forms.CharField(initial=lingot.numero, disabled=True)
        form.fields['poids_brut'] = forms.DecimalField(initial=lingot.age, disabled=True)
        form.fields['poids_immerge'] = forms.DecimalField(initial=lingot.height, disabled=True)


# class MultipleAttachmentsField(forms.Field):
#     widget = forms.FileInput(attrs={'multiple': True})

#     def clean(self, value):
#         if value is None:
#             return None

#         attachments = []
#         for file in value:
#             piecejointe = PieceJointe(file=file)
#             piecejointe.clean()
#             piecejointe.append(piecejointe)

#         return attachments




def attachment_validation_logic(form, field_name, message=None):
    message = message if message else "Impossible de faire modifications tant que la version signé est jointe."
    if form.has_changed() and form.instance.pk is not None:
        # Form data has changed, and it's not a new instance
        file_field = form.cleaned_data.get(field_name, False)
        if not getattr(form.instance, field_name) is None and file_field:
            if not (field_name in form.changed_data and len(form.changed_data) == 1) or\
                field_name not in form.changed_data:
                raise ValidationError(message)

class PayementAdminFrom(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PayementAdminFrom, self).__init__(*args, **kwargs)
        
    class Meta:
        model = Payement
        exclude = ['direction', 'user', 'archived', 'actif', 'confirme', 'fichetarification']
        readonly_fields = ['user', 'fournisseur', 'numero']
    
    def clean(self) -> dict[str, Any]:
        attachment_validation_logic(self, 'recu_payement')
        return super().clean()
    
class FactureInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        for form in self.forms:
            cleaned_data = form.cleaned_data
            print('form.instance:', form.instance)
            print('cleaned_data.items()', cleaned_data.items())
            attachment_validation_logic(form, 'facture_signe')
            # facture_attachment_validation_logic(cleaned_data, form.instance)

class FactureDefitiveInlineFormSet(FactureInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(FactureDefitiveInlineFormSet, self).__init__(*args, **kwargs)
        self.cleaned_data['type_de_facture'] = 'definitive'

    def clean(self):
        super(FactureDefitiveInlineFormSet, self).clean()
        for form in self.forms:
            form.cleaned_data['type_de_facture'] = "definitive"
        
        return self.cleaned_data
          

class FactureAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FactureAdminForm, self).__init__(*args, **kwargs)

        if self.instance.pk:
            # Si l'instance de Fichecontrol existe déjà, recuperer ajouter ses lingots
            self.fields['numero'].disabled = True
            self.fields['vente'].disabled = True

    class Meta:
        model = Facture
        exclude = ['user', 'archived']
        

    def clean(self):
        cleaned_data = super().clean()
        attachment_validation_logic(self, 'facture_signe')
        return cleaned_data

    # def clean(self):
    #     cleaned_data = super().clean()

    #     if self.instance.pk:
    #         selected_lingots = cleaned_data.get('lingots')
    #         if selected_lingots:
    #             existing_factureproforma = Lingot.objects.filter(
    #                 id__in=selected_lingots.values_list('id', flat=True),
    #                 facture_proforma__isnull=False
    #             ).exclude(facture_proforma=self.instance).values_list('facture_proforma__id', flat=True).distinct()
    #             if len(existing_factureproforma) >= 1:
    #                 raise forms.ValidationError(
    #                     'Au moins un des lingots selectionnés est deja associé à une fiche de control differente.'
    #                 )

    #     return cleaned_data

    # def save(self, commit=False, *args, **kwargs):
    #     instance = super(FactureAdminForm, self).save(commit=False)

    #     # Save the instance if it's not yet saved
    #     if not instance.pk:
    #         instance.save()
    #     else:
    #         self.fields['lingots'].initial.update(facture_proforma=None)

    #     # if self.user and not instance.user:
    #     #     instance.user = self.user
    #     if commit:
    #         instance.save()

    #     # Disassociate lingots from this Fichecontrol
    #     Lingot.objects.filter(facture_proforma=instance).update(facture_proforma=None)

    #     # Associate selected lingots with this Fichecontrol
    #     selected_lingots = self.cleaned_data.get('lingots')
    #     if selected_lingots is not None:
    #         selected_lingots.update(facture_proforma=instance)

    #     return instance

class VenteAdminForm(forms.ModelForm):

    lingots = forms.ModelMultipleChoiceField(
        queryset=Lingot.objects.filter(vente__isnull=True),
        required=False,
        help_text="Maintenez la touche 'Ctrl', ou 'Command' sur un Mac, enfoncée pour en sélectionner plusieurs."
    )

    controls = forms.ModelMultipleChoiceField(
        queryset=Control.objects.filter(),
        required=False,
        label="Controls associés",
    )

    class Meta:
        model = Vente
        fields = [ 'numero', 'client', 'vendre_selon', 'objet', 'lingots', 'controls', 'observation']

    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)

        # if self.fields['lingots']:
        #     self.fields['lingots'].disabled = True
        # Replace 'related_model_field' with the actual name of your ForeignKey field
        if self.fields.get('numero', None):
            self.fields['numero'].disabled = True

        if 'facture_proforma' in self.fields:
            # self.fields['facture_proforma'].disabled = True
            self.fields['facture_proforma'].widget.can_add_related = True
            self.fields['facture_proforma'].widget.can_delete_related = False
            self.fields['facture_proforma'].widget.can_view_related = False
        
        if 'rapport_affinage' in self.fields:
            self.fields['rapport_affinage'].disabled = True
            self.fields['rapport_affinage'].widget.can_add_related = True
            self.fields['rapport_affinage'].widget.can_delete_related = False
            self.fields['rapport_affinage'].widget.can_view_related = False
        
        if 'facture_definitive' in self.fields:
            self.fields['facture_definitive'].disabled = True
            self.fields['facture_definitive'].widget.can_add_related = True
            self.fields['facture_definitive'].widget.can_delete_related = False
            self.fields['facture_definitive'].widget.can_view_related = False
        
        if self.instance.pk:
            # Retrieve and add the lingots associated with this Fichecontrol
            lingots_set = self.instance.lingot_set.all()
            if self.fields['lingots']:
                self.fields['lingots'].initial = lingots_set
                self.fields['lingots'].queryset = self.fields['lingots'].queryset | self.fields['lingots'].initial
            if self.fields['controls']:
                self.fields['controls'].disabled = True
                all_controls = Control.objects.all()
                controls_free = all_controls.filter(
                        vente__isnull=True
                    )
                controls_lingot = all_controls.filter(
                    type_de_control=self.instance.vendre_selon,
                    controllingot__lingot_id__in=self.instance.lingot_set.all().values_list('id', flat=True)
                )
                # controls = self.instance.control_set.all()
                self.fields['controls'].queryset = (controls_free | controls_lingot).distinct('id')
                self.fields['controls'].initial = controls_lingot.distinct('id')    

    def clean(self):
        super().clean()
        
        selected_lingots = self.cleaned_data['lingots']
        already_sold_lingots = Lingot.objects.filter(
            vente__isnull=False
        )
        if self.instance.pk:
            already_sold_lingots = already_sold_lingots.exclude(vente=self.instance)
        
        already_sold_lingots = already_sold_lingots.filter(
            id__in=selected_lingots.values_list('id', flat=True)
        ).distinct()
        
        if len(already_sold_lingots) >= 1:
            print('already_sold_lingots', already_sold_lingots)
            errors = [format_html('Certains lingots sont dejà a associés a une vente.<br>')]
            errors += [format_html(f'Lingot: {l} <-> Vente: {l.vente}') for l in already_sold_lingots]
            raise forms.ValidationError(errors)

        vendre_selon = self.cleaned_data['vendre_selon']

        # Warning pour les lingots non controlés
        not_controlled_lingots = selected_lingots.exclude(
            controllingot__control__type_de_control=vendre_selon
        ).distinct()

        if not len(not_controlled_lingots) == 0:
            errors = [format_html(f"Certains lingots n'ont pas fait l'objet de {dict(TYPE_CONTROL).get(vendre_selon, None)}")]
            lingots_list = [format_html(f'<br>{l}') for l in not_controlled_lingots]

            params = '&l='.join(map(str, not_controlled_lingots.values_list('pk', flat=True)))

            # Redirect to the add form for ModelA with the initial values
            lien_create_control = reverse('gesco:commercial_control_add') + f'?l={params}&t={vendre_selon}'

            message_ajout_control = format_html(
                '<br><a target="blank" class="button" href={}>Faire le control pour ces lingot puis revenir rafrachir cette page.</a>',
                lien_create_control
            )
            errors += [message_ajout_control, lingots_list]
            raise forms.ValidationError(errors)

        # Empecher de vendre des lingots appartenant au meme control Bumigeb separament
        if vendre_selon == "bumigeb":
            controls_lingot = Control.objects.filter(
                type_de_control=vendre_selon,
                controllingot__lingot__in=selected_lingots
            ).distinct('id')

            omitted_lingots = Lingot.objects.filter(
                controllingot__control__in=controls_lingot,
                controllingot__control__type_de_control=vendre_selon
            ).exclude(
                id__in=selected_lingots.values_list('id', flat=True)
            )
            if not len(omitted_lingots) == 0:
                errors = [
                    f"Vous ne pouvez vendre séparément des lingots appartenant au même contrôle: {dict(TYPE_CONTROL).get(vendre_selon)}"
                ]

                errors += ['Les lingots suivants ont été omis:']

                for l in omitted_lingots:
                    ctl = Control.objects.filter(controllingot__lingot=l, type_de_control="bumigeb").first()
                    errors += [f'Lingot: {l} <--> {ctl}' for l in omitted_lingots]

                raise forms.ValidationError(errors)

        return self.cleaned_data

    def save(self, commit=True, *args, **kwargs):
        instance = super(VenteAdminForm, self).save(commit=commit)
        if not instance.pk:
            instance.save()
        data = self.cleaned_data
        # Associate selected lingots nd corresponding cotrols with this Vente
        
        if data['lingots'] is not None:
            # Dissociate lingots not present in the new set
            dissociated_lingot = self.instance.lingot_set.exclude(
                id__in=data['lingots'].values_list('id', flat=True)
            ).update(vente=None)
            
            # Select associted conrols according to type_de_control
            controls = Control.objects.filter(
                type_de_control=self.instance.vendre_selon,
                controllingot__lingot_id__in=data['lingots'].values_list('id', flat=True)
            ).distinct('id')
                
            data['lingots'].update(vente=instance)
            controls.update(vente=instance)

        return instance

class ControlInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        for form in self.forms:
            cleaned_data = form.cleaned_data
            print('form.instance:', form.instance)
            print('cleaned_data.items()', cleaned_data.items())
            attachment_validation_logic(form, 'document_signe')
            # facture_attachment_validation_logic(cleaned_data, form.instance)


class PourcentageSubstanceControlLingotFormset(forms.BaseInlineFormSet):

    def clean(self):
        cleaned_data = super().clean()
        total_pourcentage = 0
        reste_count = 0

        for form in self.forms:
            print(
                "PourcentageSubstanceControlLingotFormset::clean():::form.cleaned_data.get('pourcentage')",
                form.cleaned_data.get('pourcentage')
            )
            if not form.cleaned_data.get('DELETE'):
                pourcentage = form.cleaned_data.get('pourcentage') or 0

                if form.cleaned_data.get('reste'):
                    reste_count += 1
                else:
                    total_pourcentage += pourcentage

        if reste_count > 1:
            raise forms.ValidationError('Vous ne pouvez pas désigner plusieurs substance comme reste.')

        reste_percentage = 0
        if reste_count == 1:
            # Calculate the percentage for the metal with reste=True
            reste_percentage = 100 - total_pourcentage
            if reste_percentage < 0 or reste_percentage > 100:
                raise forms.ValidationError('Le total des pourcentages doit être égal à (100).')

            # Set the calculated percentage in the form
            for form in self.forms:
                if not form.cleaned_data.get('DELETE') and form.cleaned_data.get('reste'):
                    print("called set!!")
                    form.cleaned_data['pourcentage'] = reste_percentage
        if total_pourcentage + reste_percentage != 100:
            raise forms.ValidationError('Le total des pourcentages doit être égal à 100.')

        return cleaned_data

    def save(self, commit=True):
        super().save(commit=commit)
        instances = PourcentageSubstanceControlLingot.objects.filter(control_lingot=self.instance)
        for form in self.forms:
            print(form.cleaned_data['pourcentage'])
            print(form.cleaned_data['id'])
            # Perform any modifications to the instance before saving
            if form.cleaned_data.get('reste', False):
                instance = instances.filter(id=form.cleaned_data['id'].id).first()
                instance.pourcentage = form.cleaned_data['pourcentage']
                instance.reste = True
                instance.save()
        # Set the auto computed pourcentage for the reste substance
        # Setting it in the clean() does not persit it the db


class PeseeInlineFormset(forms.BaseInlineFormSet):

    def clean(self):
        cleaned_data = super().clean()
        
class PourcentageSubstanceLingotFormset(forms.BaseInlineFormSet):

    def clean(self):
        cleaned_data = super().clean()
        total_pourcentage = 0
        reste_count = 0
        # Check if at least one form is provided
        if not any(form.has_changed() for form in self.forms) and self.is_bound:
            return
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
        if total_pourcentage + reste_percentage != 100:
            raise forms.ValidationError('Le total des pourcentages doit être égal à 100.')

        return cleaned_data

    def save(self, commit=True):
        super().save(commit=commit)

class ControlAdminForm(forms.ModelForm):

    lingots = forms.ModelMultipleChoiceField(
        queryset=stock_queryset(),
        required=False,
        help_text="Maintenez la touche 'Ctrl', ou 'Command' sur un Mac, enfoncée pour en sélectionner plusieurs."
    )

    class Meta:
        model = Control
        fields = ['date_control', 'type_de_control', 'control_client', 'structure_de_control', 'vente', 'observation', 'lingots', 'document_signe', 'numero_de_control']
        readonly_fields = ['numero_de_control']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.instance.pk:
            # Retrieve and add the lingots associated with this Control to the queryset
            lingots_set = Lingot.objects.filter(
                controllingot__in=self.instance.controllingot_set.all(),
                controllingot__type_de_control=self.instance.type_de_control
                ).distinct()
            if self.fields['lingots']:
                self.fields['lingots'].initial = lingots_set
            if self.fields['type_de_control']:
                self.fields['type_de_control'].disabled = True
            
            if self.fields['date_control']:
                self.fields['date_control'].disabled = True
            
            if self.fields['vente'] and self.fields.get('vente', None):
                self.fields['vente'].disabled = True

            # if self.fields['controls']:
            #     self.fields['controls'].disabled = True
            #     controls = Control.objects.\
            #         filter(
            #             controllingot__lingot_id__in=self.instance.lingot_set.all().values_list('id', flat=True)
            #         ).distinct('id') 
            #     if len(controls) > 0:
            #         self.fields['controls'].queryset = self.fields['controls'].queryset.union(controls)
            #         self.fields['controls'].initial = controls
            pass
            
    
    def clean(self):
        cleaned_data = super().clean()
        attachment_validation_logic(self, 'document_signe')
        return cleaned_data
    # def clean(self):
    #     cleaned_data = super().clean()

    #     if self.instance.pk:
    #         selected_lingots = cleaned_data.get('lingots')
    #         if selected_lingots:
    #             already_sold_lingots = Lingot.objects.filter(
    #                 id__in=selected_lingots.values_list('id', flat=True),
    #                 vente__isnull=False
    #             ).exclude(vente=self.instance).distinct()
    #             if len(already_sold_lingots) >= 1:
    #                 errors = ['Certains lingots sont dejà a associés a une vente.']
    #                 errors += [f'Lingot: {l} <-> Vente: {l.vente}' for l in already_sold_lingots]
    #                 raise forms.ValidationError(errors)

    #     return cleaned_data
    
class MouvementLingotAdminFormSave(forms.ModelForm):
    lingots = forms.ModelMultipleChoiceField(
        queryset=stock_queryset(),
        required=False,
        help_text="Maintenez la touche 'Ctrl', ou 'Command' sur un Mac, enfoncée pour en sélectionner plusieurs."
    )

    class Meta:
        model = MouvementLingot
        fields = ['etat', 'lingots']

    def __init__(self, *args, **kwargs):
        super(MouvementLingotAdminForm, self).__init__(*args, **kwargs)
        print('in init():')
        print(self.fields['lingots'])
        self.fields['lingots'].widget = RelatedFieldWidgetWrapper(
            self.fields['lingots'].widget,
            Pesee._meta.get_field('lingot').remote_field,
            CommercialAdmin(name='gesco'),
            can_delete_related=True,
            can_add_related=True,
            can_change_related=True,
        )

        if self.instance.pk:
            # Retrieve and add the lingots associated with this Fichecontrol
            self.fields['lingots'].initial = self.instance.lingots.all()
            self.fields['lingots'].queryset = self.fields['lingots'].queryset | self.fields['lingots'].initial
        
        if 'lingots' in self.fields:
            self.fields['lingots'].disabled = True
            self.fields['lingots'].widget.can_add_related = False
            self.fields['lingots'].widget.can_delete_related = False
            self.fields['lingots'].widget.can_view_related = False

    def clean(self):
        cleaned_data = super().clean()

        # TODO check on going movement
        if self.instance.pk:
            selected_lingots = cleaned_data.get('lingots')
            if selected_lingots:
                selected_lingots_list = selected_lingots.values_list('id', flat=True)
                ongoing_movements = MouvementLingot.objects.filter(lingots__id__in=selected_lingots_list, etat='start').values_list('lingots__id', flat=True)
                if len(ongoing_movements) >= 1:
                    raise forms.ValidationError(
                        'Certains lingots sont en cours de deplacementt:'
                    )
                
        return cleaned_data

    
    
class MouvementLingotAdminForm(forms.ModelForm):
    lingots_a_deplacer = forms.ModelMultipleChoiceField(
        queryset=stock_queryset(),
        required=False,
        help_text="Maintenez la touche 'Ctrl', ou 'Command' sur un Mac, enfoncée pour en sélectionner plusieurs."
    )

    class Meta:
        model = MouvementLingot
        fields = ['etat', 'destination', 'lingots_a_deplacer']

    def __init__(self, *args, **kwargs):
        super(MouvementLingotAdminForm, self).__init__(*args, **kwargs)
        self.fields['lingots_a_deplacer'].widget = RelatedFieldWidgetWrapper(
            self.fields['lingots_a_deplacer'].widget,
            Pesee._meta.get_field('lingot').remote_field,
            CommercialAdmin(name='gesco'),
            can_delete_related=True,
            can_add_related=True,
            can_change_related=True,
        )

        if self.instance.pk:
            # Retrieve and add the lingots associated with this Fichecontrol
            unique_lingots = Lingot.objects.filter(mouvementlingot=self.instance)
            self.fields['lingots_a_deplacer'].initial = unique_lingots

        if 'lingots_a_deplacer' in self.fields:
            self.fields['lingots_a_deplacer'].disabled = False
            self.fields['lingots_a_deplacer'].widget.can_add_related = True
            self.fields['lingots_a_deplacer'].widget.can_delete_related = False
            self.fields['lingots_a_deplacer'].widget.can_view_related = False

    def clean(self):
        cleaned_data = super().clean()

        # TODO check on-going movement
        selected_lingots = cleaned_data.get('lingots_a_deplacer')
        print("self.fields['lingots_a_deplacer'].queryset", self.fields['lingots_a_deplacer'].queryset)
        print('selected lingot in form clean:', selected_lingots)
        selected_lingots_list = None
        if selected_lingots:
            selected_lingots_list = selected_lingots.values_list('id', flat=True)
        if selected_lingots_list and len(selected_lingots) > 0:
            if self.instance.pk:
                ongoing_movements = MouvementLingot.objects.exclude(pk=self.instance.pk)\
                    .filter(lingots__id__in=selected_lingots_list, etat='start')
            else:
                ongoing_movements = MouvementLingot.objects\
                    .filter(lingots__id__in=selected_lingots_list, etat='start')
            if len(ongoing_movements) >= 1:
                    error_message = ['Certains lingots sont en cours de déplacement:']
                    for mv in ongoing_movements:
                        print('mv:', mv)
                        for l in mv.lingots.all():
                            print('l:', l)
                            error_message.extend([f'{l} --> {mv}'])
                    raise forms.ValidationError(
                        error_message
                    )

        return cleaned_data

    def save(self, *args, **kwargs):
        instance = super(MouvementLingotAdminForm, self).save(commit=False)
        instance.save()
        self.save_m2m()
        return instance
    
class SMSAdminForm(forms.ModelForm):
    class Meta:
        model = SMS
        exclude = ['type_de_message', 'envoye']

    def __init__(self, *args, **kwargs):
        super(SMSAdminForm, self).__init__(*args, **kwargs)

    def save(self, *args, commit=True, **kwargs):
        instance = super(SMSAdminForm, self).save(commit=False)
        return instance

    def clean(self):
        cleaned_data = super().clean()

        # Access the 'envoye' value from the instance
        envoye_value = self.instance.envoye if self.instance else False

        # If 'envoye' is True, prevent modification of 'fournisseurs' and 'client'
        if envoye_value:
            if self.fields.get('fournisseurs', None):
                self.fields['fournisseurs'].disabled = True
            if self.fields.get('fournclientsisseurs', None):
                self.fields['clients'].disabled = True

        return cleaned_data         