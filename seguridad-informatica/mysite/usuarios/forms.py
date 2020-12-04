from django import forms
from .models import ValidacionCodigo

class ValidacionCodigoForm(forms.ModelForm):
    codigo = forms.CharField(max_length=8, widget=forms.HiddenInput())
    codigo_ingresado = forms.CharField(max_length=8)
    usuario = forms.CharField(widget=forms.HiddenInput())
    date_init = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = ValidacionCodigo
        fields = ['codigo', 'codigo_ingresado', 'usuario', 'date_init']
    
