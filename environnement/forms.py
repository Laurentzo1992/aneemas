from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from paramettre.models import *
from django.core.validators import RegexValidator


class FicheprelevementsForm(forms.ModelForm):
    class Meta:
        model = Ficheprelevements
        fields = '__all__'
        
        widgets = {
            'motif': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'nom_personnes_commandiaire': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'adresse_personnes_commandiaire': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'date_prelevement': forms.DateInput(attrs={'type': 'date'}),
        }
