# forms.py
from django import forms
from .models import *
 
 
class SearchForm(forms.ModelForm):
 
    class Meta:
        model = Search
        fields = '__all__'