from django import forms
from .models import *


class ApiImageForm(forms.ModelForm):

    class Meta:
        model = ApiImage
        fields = ['name', 'Main_Img']
