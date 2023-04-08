from django import forms
#from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User
from .models import Psych_D_symptoms, Disorder_Diagnosis


class Symptoms(forms.ModelForm):
    #disorders = forms.CharField(label="Select disorder",
    #widget=forms.Select(choices=Disorder_choices))

    class Meta:
        model = Psych_D_symptoms
        fields = ('symptom_name', 'symptom_desc', 'symptom_keywords')

class Diagnosis(forms.ModelForm):

    class Meta:
        model = Disorder_Diagnosis
        fields = ('disorder_desc', 'disorder_keywords', 'symptoms', 'recommendation')
        
    


    
    #description = forms.CharField(max_length=500)
    #Symptom = forms.CharField(max_length=255)

