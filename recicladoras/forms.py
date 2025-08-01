# recicladoras/forms.py
import os
from django import forms
# from core.models import TipoMaterialReciclable
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
# class TipoMaterialReciclableForm(forms.ModelForm):
#     class Meta:
#         model = TipoMaterialReciclable
#         fields = ['nombre', 'descripcion', 'tiempo_descomposicion', 'imagen']

#     def __init__(self, *args, **kwargs):
#         is_update = kwargs.pop('is_update', False)
#         super().__init__(*args, **kwargs)
#         for field in self.fields.values():
#             field.widget.attrs.update({'class': 'form-control'})
#         if is_update:
#             self.fields['imagen'].required = False
#         else:
#             self.fields['imagen'].required = True

#     def clean_imagen(self):
#         imagen = self.cleaned_data.get('imagen')
#         if imagen:
#             ext = os.path.splitext(imagen.name)[1].lower()
#             if ext not in ['.jpg', '.jpeg', '.png']:
#                 raise forms.ValidationError("Sólo se permiten imágenes JPG, JPEG o PNG.")
#             if imagen.size > 10 * 1024 * 1024:
#                 raise forms.ValidationError("La imagen no debe superar los 10MB.")
#         return imagen

