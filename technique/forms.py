from django import forms
from django.contrib.gis import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from paramettre.models import *
from django.core.validators import RegexValidator
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field


### FORM ENROLEMENT ###

class EnrolementForm(forms.ModelForm):
    
    
    class Meta:
        model = Fichenrolements
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'type_carte': forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-select-multiple'}),
        }
        
        

class FichevisitesForm(forms.ModelForm):
    
    date_visite = forms.DateField(
    widget=forms.TextInput(     
        attrs={'type': 'date'} 
        )
        ) 
    
    date_miss = forms.DateField(
    widget=forms.TextInput(     
        attrs={'type': 'date'} 
        )
        ) 
    
    
    
    class Meta:
        model = Fichevisites
        fields = '__all__'
        widgets = {
            'nom_des_visiteurs': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }
        



class FormguidautoritesForm(forms.ModelForm):
    
    
   
    class Meta:
        model = Formguidautorites
        fields = '__all__'
        
        widgets = {
            'date_visite': forms.DateInput(attrs={'type': 'date'}),
            'date_miss': forms.DateInput(attrs={'type': 'date'}),
            'personne': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'personne2': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'adresse': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }
        
        
        
class DemandeconventionsForm(forms.ModelForm):
    reconnaissance = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    concertation = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    organisation = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    plan_masse = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    pv_constat = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    
    fournisseur = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    exploitant = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))


    class Meta:
        model = Demandeconventions
        fields = '__all__'
        
        widgets = {
            'substances': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'date_depot': forms.DateInput(attrs={'type': 'date'}),
            'date_signature': forms.DateInput(attrs={'type': 'date'}),
            'date_effet_sign': forms.DateInput(attrs={'type': 'date'}),
            'date_exp': forms.DateInput(attrs={'type': 'date'}),
            'date_premier_vers': forms.DateInput(attrs={'type': 'date'}),
            'date_relance': forms.DateInput(attrs={'type': 'date'}),
            'type_autorisation': forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-select-multiple'}),
        }
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Field('reconnaissance', css_class='form-check-input'),
            Field('concertation', css_class='form-check-input'),
            Field('organisation', css_class='form-check-input'),
            Field('plan_masse', css_class='form-check-input'),
            Field('pv_constat', css_class='form-check-input'),
            
            Field('fournisseur', css_class='form-check-input'),
            Field('exploitant', css_class='form-check-input'),
            # Ajoutez d'autres champs ici selon vos besoins
        )
        
        
        


class FormincidentsForm(forms.ModelForm):
    class Meta:
        model = Formincidents
        fields = '__all__'
        
        widgets = {
            'heure_incident': forms.TimeInput(attrs={'type': 'time'}),
            'equipement_implique': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'personne_implique': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'cause': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'action_corrective': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'mesure_de_securite': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'date_incident': forms.DateInput(attrs={'type': 'date'}),
            'type_autorisation': forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-select-multiple'}),
        }




class RapactivitesForm(forms.ModelForm):
    class Meta:
        model = Rapactivites
        fields = '__all__'
        
        widgets = {
            'autre1': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'autre': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'obs': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'cause': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'action_corrective': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'mesure_de_securite': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'periode1': forms.DateInput(attrs={'type': 'date'}),
            'periode2': forms.DateInput(attrs={'type': 'date'}),
            'type_cart_art': forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-select-multiple'}),
        }


class ComsitesForm(forms.ModelForm):
    class Meta:
        model = Comsites
        fields = '__all__'
        
        widgets = {
            
            'obs_geo': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'machine': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'date_deb_expl': forms.DateInput(attrs={'type': 'date'}),
            'date_fin_exp': forms.DateInput(attrs={'type': 'date'}),
        }
        
