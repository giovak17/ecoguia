from django import forms
from core.models import Usuarios, Roles, TipoMaterialReciclable
from django.core.exceptions import ValidationError
from django.utils import timezone
import os


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = '__all__'
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'fecha_registro': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        self.fields['id_rol'].queryset = Roles.objects.all()
        self.fields['id_rol'].label_from_instance = lambda obj: obj.nombre

        # Hacer ciertos campos obligatorios desde el formulario
        self.fields['nombre'].required = True
        self.fields['ap_paterno'].required = True
        self.fields['correo'].required = True
        self.fields['id_rol'].required = True

    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')
        if fecha_nacimiento and fecha_nacimiento > timezone.now().date():
            raise ValidationError("La fecha de nacimiento no puede ser en el futuro.")
        return fecha_nacimiento

    def clean_fecha_registro(self):
        fecha_registro = self.cleaned_data.get('fecha_registro')
        if fecha_registro and fecha_registro > timezone.now():
            raise ValidationError("La fecha de registro no puede ser en el futuro.")
        return fecha_registro

class TipoMaterialReciclableForm(forms.ModelForm):
    class Meta:
        model = TipoMaterialReciclable
        fields = ['nombre', 'descripcion', 'tiempo_descomposicion', 'imagen']

    def __init__(self, *args, **kwargs):
        is_update = kwargs.pop('is_update', False)
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        if is_update:
            self.fields['imagen'].required = False
        else:
            self.fields['imagen'].required = True

    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen')
        if imagen:
            ext = os.path.splitext(imagen.name)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png']:
                raise forms.ValidationError("Sólo se permiten imágenes JPG, JPEG o PNG.")
            if imagen.size > 10 * 1024 * 1024:
                raise forms.ValidationError("La imagen no debe superar los 10MB.")
        return imagen

