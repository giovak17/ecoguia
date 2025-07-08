from django import forms
from .models import SolicitudRegistro

class SolicitudRegistroForm(forms.ModelForm):
    class Meta:
        model = SolicitudRegistro
        fields = '__all__'
        exclude = ['aprobado']  # ocultamos esto para que solo el admin lo modifique
