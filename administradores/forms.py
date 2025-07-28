from django import forms
from core.models import Usuarios, Roles
from django.core.exceptions import ValidationError
from django.utils import timezone

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
