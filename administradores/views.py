from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from core.models import Recicladoras
from core.models import Usuarios, Roles
from django.contrib import messages
from core.models import ContenidoEducativo
from usuarios.views import convertir_a_embed
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import user_passes_test
from core.auth import login_required
import re

# Create your views here.

@login_required(role="administrador")
def index(request):
    return render(request, "administradores/index.html")

def ver_recicladoras(request):
    recicladoras = Recicladoras.objects.select_related('propietario').all()
    return render(request, 'administradores/recicladoras.html', {'recicladoras': recicladoras})
def recicladora_crear(request):
    errores = {}
    recicladora_data = {}
    propietarios = Usuarios.objects.all()
    reciclador_rol = Roles.objects.get(nombre='Recicladora')
    propietarios = Usuarios.objects.filter(id_rol=reciclador_rol)



    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        propietario_id = request.POST.get('propietario')
        calle = request.POST.get('calle')
        colonia = request.POST.get('colonia')
        ciudad = request.POST.get('ciudad')
        codigo_postal = request.POST.get('codigo_postal')
        numero_int = request.POST.get('numero_int')
        telefono = request.POST.get('numero_telefonico')

        recicladora_data = {
            'nombre': nombre,
            'propietario_id': propietario_id,
            'calle': calle,
            'colonia': colonia,
            'ciudad': ciudad,
            'codigo_postal': codigo_postal,
            'numero_int': numero_int,
            'numero_telefonico': telefono,
        }

        if not nombre:
            errores['nombre'] = 'El nombre es obligatorio'
        if not ciudad:
            errores['ciudad'] = 'La ciudad es obligatoria'

        if not errores:
            Recicladoras.objects.create(
                nombre=nombre,
                propietario_id=propietario_id or None,
                calle=calle,
                colonia=colonia,
                ciudad=ciudad,
                codigo_postal=codigo_postal or None,
                numero_int=numero_int or None,
                numero_telefonico=telefono
            )
            return redirect('administradores:ver_recicladoras')

    return render(request, 'administradores/recicladora_form.html', {
        'errores': errores,
        'titulo': 'Registrar Recicladora',
        'propietarios': propietarios,
        'recicladora': recicladora_data
    })



def recicladora_editar(request, pk):
    recicladora = get_object_or_404(Recicladoras, pk=pk)
    errores = {}

    from core.models import Usuarios 

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        ciudad = request.POST.get('ciudad')
        telefono = request.POST.get('numero_telefonico')
        calle = request.POST.get('calle')
        colonia = request.POST.get('colonia')
        numero_int = request.POST.get('numero_int')
        codigo_postal = request.POST.get('codigo_postal')
        aprobada = request.POST.get('aprobada') == 'on'
        propietario_id = request.POST.get('propietario')

        if not nombre:
            errores['nombre'] = 'El nombre es obligatorio'
        if not ciudad:
            errores['ciudad'] = 'La ciudad es obligatoria'

        if not errores:
            recicladora.nombre = nombre
            recicladora.ciudad = ciudad
            recicladora.numero_telefonico = telefono or None
            recicladora.calle = calle or None
            recicladora.colonia = colonia or None
            recicladora.numero_int = numero_int or None
            recicladora.codigo_postal = codigo_postal or None
            recicladora.aprobada = aprobada
            recicladora.propietario_id = propietario_id or None
            recicladora.save()
            return redirect('administradores:ver_recicladoras')

 
    propietarios = Usuarios.objects.all()

    return render(request, 'administradores/recicladora_form.html', {
        'recicladora': recicladora,
        'errores': errores,
        'propietarios': propietarios,
        'titulo': 'Editar Recicladora'
    })

def recicladora_eliminar(request, pk):
    recicladora = get_object_or_404(Recicladoras, pk=pk)
    if request.method == 'POST':
        recicladora.delete()
        return redirect('administradores:ver_recicladoras')
    return render(request, 'administradores/recicladoras_confirm_delete.html', {'recicladora': recicladora})


def listar_usuarios(request):
    usuarios = Usuarios.objects.all()
    return render(request, 'administradores/listado_usuarios.html', {'usuarios': usuarios})
  
@login_required(role="administrador")
def aprobar_recicladoras(request: HttpRequest):
    success = False
    if request.method == "POST":
        post_data = request.POST.copy().dict()
        post_data.pop('csrfmiddlewaretoken', None)

        # Por cada una de las recicladoras, actualizar el estado de "aprobado" al estado recibido por el formulario
        for key, val in post_data.items():
            rec = Recicladoras.objects.get(pk=int(key))

            if val == "True":
                rec.aprobada = True
            else:
                rec.aprobada = False
            rec.save()
            success = True

    recicladoras = Recicladoras.objects.select_related("propietario").order_by("-codigo_recicladora");

    return render(request, "administradores/aprobar_recicladoras.html", {"recicladoras":recicladoras, "success": success })

# Solo admins pueden entrar


# @user_passes_test(lambda u: u.is_staff)
def validar_campos(titulo, descripcion, videos):
    errores = {}

    # Validar título
    if not titulo:
        errores['titulo'] = "El título es obligatorio."
    elif len(titulo) > 25:
        errores['titulo'] = "El título no debe exceder 25 caracteres."

    # Validar descripción
    if not descripcion:
        errores['descripcion'] = "La descripción es obligatoria."
    elif len(descripcion) < 10:
        errores['descripcion'] = "La descripción debe tener al menos 10 caracteres."

    # Validar enlace de video (si existe)
    if videos and not videos.startswith(('http://', 'https://')):
        errores['videos'] = "El enlace de video debe ser una URL válida."

    # Si hay errores, lanzar excepción
    if errores:
        raise ValidationError(errores)

def contenido_educativo_admin(request):
    contenidos = ContenidoEducativo.objects.all()
    for contenido in contenidos:
        if contenido.videos:
            contenido.videos_embed = convertir_a_embed(contenido.videos)
    return render(request, 'administradores/contenido_educativo_admin.html', {'contenidos': contenidos})

def contenido_crear(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        id_usuario_ce = request.user.id  # o lo que uses para relacionar usuario
        imagen = request.FILES.get('imagen')
        videos = request.POST.get('videos')
        video_local = request.FILES.get('video_local')

        nuevo = ContenidoEducativo(
            titulo=titulo,
            descripcion=descripcion,
            id_usuario_ce_id=id_usuario_ce,
            imagen=imagen,
            videos=videos,
            video_local=video_local
        )
        try:
            validar_campos(titulo, descripcion, videos)
            nuevo.clean()
            nuevo.save()
            return redirect('administradores:contenido_admin')
        except ValidationError as e:
            errores = e.message_dict
            # envía errores al template
            return render(request, 'administradores/contenido_form.html', {'errores': errores, 'contenido': nuevo})

    return render(request, 'administradores/contenido_form.html')

def contenido_editar(request, pk):
    contenido = get_object_or_404(ContenidoEducativo, pk=pk)

    if request.method == 'POST':
        contenido.titulo = request.POST.get('titulo')
        contenido.descripcion = request.POST.get('descripcion')
        contenido.videos = request.POST.get('videos')

        if 'imagen' in request.FILES:
            contenido.imagen = request.FILES['imagen']
        if 'video_local' in request.FILES:
            contenido.video_local = request.FILES['video_local']

        try:
            validar_campos(contenido.titulo, contenido.descripcion, contenido.videos)
            contenido.clean()
            contenido.save()
            return redirect('administradores:contenido_admin')
        except ValidationError as e:
            errores = e.message_dict
            return render(request, 'administradores/contenido_form.html', {'errores': errores, 'contenido': contenido})

    return render(request, 'administradores/contenido_form.html', {'contenido': contenido})

def contenido_borrar(request, pk):
    contenido = get_object_or_404(ContenidoEducativo, pk=pk)
    if request.method == 'POST':
        contenido.delete()
        return redirect(('administradores:contenido_admin'))
    return render(request, 'administradores/contenido_confirm_delete.html', {'contenido': contenido})