from django import forms
from paramettre.models import *
from django.core.validators import RegexValidator


### FORM ENROLEMENT ###

class EnrolementForm(forms.ModelForm):
    

    type_carte = forms.CharField(
        label='Type carte',
        widget=forms.TextInput(attrs={'placeholder': 'Type carte'})
    )


    class Meta:
        model = Fichenrolements
        fields = '__all__'
        
        
        

        