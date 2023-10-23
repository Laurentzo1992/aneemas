from django import forms
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
        
        
        

        