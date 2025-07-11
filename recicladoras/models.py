from django.db import models
from core.models import Recicladoras,TipoMaterialReciclable

# Create your models here.

class SolicitudRegistro(models.Model):
    nombre_establecimiento = models.CharField(max_length=100)
    ubicacion = models.TextField()
    horarios_atencion = models.CharField(max_length=100)
    telefono_contacto = models.CharField(max_length=20)
    materiales_aceptados = models.TextField()
    aprobado = models.BooleanField(default=False)
    
    
    

    def __str__(self):
        return self.nombre_establecimiento
