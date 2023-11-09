from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from paramettre.models import *
from django.core.validators import RegexValidator
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class FicheprelevementsForm(forms.ModelForm):
    class Meta:
        model = Ficheprelevements
        fields = '__all__'
        
        widgets = {
            'motif': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'nom_preleveur': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'nom_personnes_commandiaire': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'adresse_personnes_commandiaire': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'date_prelevement': forms.DateInput(attrs={'type': 'date'}),
        }



class FichexpminieresForm(forms.ModelForm):
    class Meta:
        model = Fichexpminieres
        fields = '__all__'
        
        widgets = {
            'q180': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'resultat': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'but_mission': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'q19': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'q21': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'type_equipement': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'type_equipement_aeration': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'type_equipement_eclairage': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'q96': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'q97': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'q98': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'q99': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'date_la_mission': forms.DateInput(attrs={'type': 'date'}),
            'd_octroi': forms.DateInput(attrs={'type': 'date'}),
            'd_renouv': forms.DateInput(attrs={'type': 'date'}),
            'd_fin': forms.DateInput(attrs={'type': 'date'}),
            'qe130': forms.DateInput(attrs={'type': 'date'}),
        }
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'

        self.helper.add_input(Submit('submit', 'Submit'))