from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from paramettre.models import *
from django.core.validators import RegexValidator


### FORM ENROLEMENT ###

class EnrolementForm(forms.ModelForm):
    
    date = forms.DateField(
    widget=forms.TextInput(     
        attrs={'type': 'date'} 
        )
        ) 
    
    
    class Meta:
        model = Fichenrolements
        fields = '__all__'
        
        

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
            'substance1': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'date_depot': forms.DateInput(attrs={'type': 'date'}),
        }
        
