from django import forms
from core.models import SolicitudRegistro, TipoMaterialReciclable


class SolicitudRegistroForm(forms.ModelForm):
    class Meta:
        model = SolicitudRegistro
        fields = '__all__'
        exclude = ['aprobado']  # ocultamos esto para que solo el admin lo modifique

class TipoMaterialReciclableForm(forms.ModelForm):
    class Meta:
        model = TipoMaterialReciclable
        fields = ['nombre', 'descripcion', 'tiempo_descomposicion']
