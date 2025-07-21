# recicladoras/forms.py
from django import forms
from core.models import TipoMaterialReciclable
from core.models import Recicladoras

# class SolicitudRecicladoraForm(forms.ModelForm):
#     class Meta:
#         model = SolicitudRegistro
#         fields = '__all__'
#         exclude = ['aprobado']  # ocultamos esto para que solo el admin lo modifique
class SolicitudRecicladoraForm(forms.ModelForm):
    class Meta:
        model = Recicladoras
        fields = [
            'nombre',
            'propietario',
            'calle',
            'codigo_postal',
            'colonia',
            'numero_int',
            'ciudad',
            'numero_telefonico'
        ]

class TipoMaterialReciclableForm(forms.ModelForm):
    class Meta:
        model = TipoMaterialReciclable
        fields = ['nombre', 'descripcion', 'tiempo_descomposicion']
        model = Recicladoras
        fields = [
            'nombre',
            'propietario',
            'calle',
            'codigo_postal',
            'colonia',
            'numero_int',
            'ciudad',
            'numero_telefonico'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
                'required': 'required'
            })
