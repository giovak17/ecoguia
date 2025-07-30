# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.core.exceptions import ValidationError


class ContenidoEducativo(models.Model):
    codigo = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=25, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    id_usuario_ce = models.ForeignKey('Usuarios', models.SET_NULL, db_column='id_usuario_ce', blank=True, null=True)
    # son campos para cargar media
    imagen = models.ImageField(upload_to='contenido/imagenes/', blank=True, null=True)
    videos= models.URLField(blank=True, null=True)
    video_local = models.FileField(upload_to='contenido/videos/', blank=True, null=True)

    def clean(self):
        super().clean()
        if not (self.imagen or self.videos or self.video_local):
            raise ValidationError("Debe subir al menos una imagen, un video local o un enlace de video.")



    class Meta:
        managed = False
        db_table = 'contenido_educativo'


class EntregaMaterialReciclado(models.Model):
    id_entrega_material = models.AutoField(primary_key=True)
    id_entrega = models.ForeignKey('Entregas', models.DO_NOTHING, db_column='id_entrega', blank=True, null=True)
    id_material = models.ForeignKey('MaterialReciclable', models.DO_NOTHING, db_column='id_material', blank=True, null=True)
    cantidad = models.IntegerField(blank=True, null=True)
    condiciones_entrega = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'entrega_material_reciclado'


class Entregas(models.Model):
    id_entrega = models.AutoField(primary_key=True)
    fecha_entrega = models.DateTimeField(blank=True, null=True)
    id_usuario_e = models.ForeignKey('Usuarios', models.SET_NULL, db_column='id_usuario_e', blank=True, null=True)
    punto_entrega = models.ForeignKey('PuntosReciclaje', models.DO_NOTHING, db_column='punto_entrega', blank=True, null=True)
    confirmada = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'entregas'


class MaterialReciclable(models.Model):
    id_material = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    tipo_reciclaje = models.ForeignKey('TipoMaterialReciclable', models.DO_NOTHING, db_column='tipo_reciclaje', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'material_reciclable'


class Publicaciones(models.Model):
    clave_publicacion = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=30, blank=True, null=True)
    contenido = models.TextField(blank=True, null=True)
    id_usuario_p = models.ForeignKey('Usuarios', models.SET_NULL, db_column='id_usuario_p', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'publicaciones'


class PuntosReciclaje(models.Model):
    id_punto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    ubicacion = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    horario_entrada = models.TimeField(blank=True, null=True)
    horario_salida = models.TimeField(blank=True, null=True)
    id_recicladora = models.ForeignKey('Recicladoras', models.DO_NOTHING, db_column='id_recicladora', blank=True, null=True)
    ciudad = models.CharField(max_length=50, blank=True, null=True)
    #se usaran para que funcione google maps 
    extras = models.TextField(blank=True, null=True)
    latitud = models.FloatField(blank=True, null=True)
    longitud = models.FloatField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'puntos_reciclaje'


class Recicladoras(models.Model):
    codigo_recicladora = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    propietario = models.ForeignKey('Usuarios', models.SET_NULL, db_column='propietario', blank=True, null=True)
    calle = models.CharField(max_length=50, blank=True, null=True)
    codigo_postal = models.IntegerField(blank=True, null=True)
    colonia = models.CharField(max_length=50, blank=True, null=True)
    numero_int = models.IntegerField(blank=True, null=True)
    ciudad = models.CharField(max_length=30, blank=True, null=True)
    numero_telefonico = models.CharField(max_length=20, blank=True, null=True)
    aprobada = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recicladoras'


class Recompensas(models.Model):
    codigo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    clave_reto = models.ForeignKey('Retos', models.DO_NOTHING, db_column='clave_reto', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recompensas'


class Retos(models.Model):
    codigo = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=30, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'retos'


class Roles(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'roles'


class TipoMaterialReciclable(models.Model):
    id_tmr  = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=40, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    tiempo_descomposicion = models.TextField(blank=True, null=True)
    imagen = models.ImageField(upload_to='clasificacion/', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipo_material_reciclable'


class Usuarios(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    ap_paterno = models.CharField(max_length=25, blank=True, null=True)
    ap_materno = models.CharField(max_length=25, blank=True, null=True)
    correo = models.CharField(max_length=100, blank=True, null=True)
    contrasena = models.CharField(max_length=20, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    fecha_registro = models.DateTimeField(blank=True, null=True)
    total_recompensas = models.IntegerField(blank=True, null=True)
    id_rol = models.ForeignKey(Roles, models.DO_NOTHING, db_column='id_rol', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuarios'


class UsuariosRecompensas(models.Model):
    pk = models.CompositePrimaryKey('id_usuario', 'id_recompensa')
    id_usuario = models.ForeignKey(Usuarios, models.DO_NOTHING, db_column='id_usuario')
    id_recompensa = models.ForeignKey(Recompensas, models.DO_NOTHING, db_column='id_recompensa')
    fecha_canjeo = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuarios_recompensas'


class UsuariosRetos(models.Model):
    pk = models.CompositePrimaryKey('id_usuario', 'id_reto')
    id_usuario = models.ForeignKey(Usuarios, models.DO_NOTHING, db_column='id_usuario')
    id_reto = models.ForeignKey(Retos, models.DO_NOTHING, db_column='id_reto')
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuarios_retos'

class SolicitudRegistro(models.Model):
    nombre_establecimiento = models.CharField(max_length=100)
    ubicacion = models.TextField()
    horarios_atencion = models.CharField(max_length=100)
    telefono_contacto = models.CharField(max_length=20)
    materiales_aceptados = models.TextField()
    aprobado = models.BooleanField(default=False)
    
class MaterialAceptado(models.Model):
    id_ma = models.AutoField(primary_key=True)
    id_punto = models.ForeignKey('PuntosReciclaje', on_delete=models.CASCADE, db_column='id_punto')
    id_tipo_material = models.ForeignKey('TipoMaterialReciclable', on_delete=models.CASCADE, db_column='id_tipo_material')

    class Meta:
        managed = False
        db_table = 'material_aceptado'
