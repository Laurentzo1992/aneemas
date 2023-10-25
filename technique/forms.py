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

    def __init__(self, *args, **kwargs):
        super(DemandeconventionsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout()

        # Nombre de colonnes dans une rangée
        colonnes_par_rangee = 4

        champ_index = 0
        row = Row()

        for champ_name, champ in self.fields.items():
            if champ_index % colonnes_par_rangee == 0:
                if champ_index > 0:
                    self.helper.layout.append(row)
                row = Row()
            
            row.append(Column(champ_name, css_class='col-3'))
            champ_index += 1

        if champ_index > 0:
            self.helper.layout.append(row)
