from django import forms
from .models import IaModel


class IaForm(forms.ModelForm):
    class Meta:
        model = IaModel
        fields = ['texto']