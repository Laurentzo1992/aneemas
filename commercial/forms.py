
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field
from .models import *
from django.forms.models import inlineformset_factory

from django.contrib import admin
from .models import Lingot, Fonte

    
class FonteForm(forms.ModelForm):
    class Meta:
        model = Fonte
        fields = ['lingots', 'date_debut', 'date_fin', 'etat']



class FicheControlForm(forms.ModelForm):
    class Meta:
        model = Fichecontrol
        fields = (
            'user',
            'observation',
            'date_control'
        )


class LingotForm(forms.ModelForm):
    class Meta:
        model = Lingot
        fields = (
            'poids_brut',
            'poids_immerge',
            'date_reception',
            'observation'
        )

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