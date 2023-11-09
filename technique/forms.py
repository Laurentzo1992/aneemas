from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from paramettre.models import *
from django.core.validators import RegexValidator


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
        
        
        
class DemandeconventionsForm(forms.ModelForm):
    class Meta:
        model = Demandeconventions
        fields = '__all__'
        
        widgets = {
            'substances': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'date_depot': forms.DateInput(attrs={'type': 'date'}),
            'type_autorisation': forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-select-multiple'}),
        }
        


class FormincidentsForm(forms.ModelForm):
    class Meta:
        model = Formincidents
        fields = '__all__'
        
        widgets = {
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
            
            'action_corrective': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'mesure_de_securite': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'date_deb_expl': forms.DateInput(attrs={'type': 'date'}),
            'date_fin_exp': forms.DateInput(attrs={'type': 'date'}),
        }