
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field
from .models import *
from django.forms.models import inlineformset_factory
from django.contrib import admin
from .models import PieceJointe


from .models import Lingot, Fonte
from django.contrib.admin.widgets import FilteredSelectMultiple, RelatedFieldWidgetWrapper

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
        if self.fields['fichecontrol']:
            self.fields['fichecontrol'].queryset = Fichecontrol.objects.filter(fichetarification__isnull=True)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "fichecontrol":  # Replace with the actual field name
            kwargs["queryset"] = Fichecontrol.objects.filter(fichetarification__isnull=True)  # Define your filter criteria here
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

class FicheControlAdminForm(forms.ModelForm):
    lingots = forms.ModelMultipleChoiceField(
        queryset=Lingot.objects.filter(fichecontrol__isnull=True),
        required=False,
        help_text="Maintenez la touche 'Ctrl', ou 'Command' sur un Mac, enfoncée pour en sélectionner plusieurs."
    )

    class Meta:
        model = Fichecontrol
        fields = ['fournisseur', 'date_control', 'lingots', 'observation']

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
            self.fields['lingots'].initial = self.instance.lingot_set.all()
            self.fields['lingots'].queryset = self.fields['lingots'].queryset | self.fields['lingots'].initial

    def clean(self):
        cleaned_data = super().clean()

        if self.instance.pk:
            selected_lingots = cleaned_data.get('lingots')
            if selected_lingots:
                existing_fichecontrols = Lingot.objects.filter(
                    id__in=selected_lingots.values_list('id', flat=True),
                    fichecontrol__isnull=False
                ).exclude(fichecontrol=self.instance).values_list('fichecontrol__id', flat=True).distinct()
                print("existing: ", existing_fichecontrols)
                if len(existing_fichecontrols) >= 1:
                    raise forms.ValidationError(
                        'Au moins un des lingots selectionnés est deja associé à une fiche de control differente.'
                    )

        return cleaned_data

    def save(self, commit=False, *args, **kwargs):
        instance = super(FicheControlAdminForm, self).save(commit=False)

        # Save the instance if it's not yet saved
        if not instance.pk:
            instance.save()
        else:
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
                print(existing_fichecontrols)
                print(len(existing_fichecontrols))

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
    class Meta:
        model = Lingot
        fields = (
            'poids_brut',
            'poids_immerge',
            'date_reception',
            'observation'
        )

        def __init__(self, *args, **kwargs):
            super(LingotAdminForm, self).__init__(*args, **kwargs)
            self.fields['date_reception'].widget.attrs['disabled'] = True
            self.fields['fournisseur'].hidden = True

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


class PayementAdminFrom(forms.ModelForm):
    # piecesjointes = forms.FileField(widget=forms.ClearableFileInput(), required=False)

    class Meta:
        model = Payement
        fields = '__all__'