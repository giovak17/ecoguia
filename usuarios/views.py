from django.http import HttpRequest, HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from core.models import Recompensas, Usuarios,Entregas
from django.shortcuts import redirect, render
from core.models import Usuarios,Entregas, PuntosReciclaje,ContenidoEducativo,EntregaMaterialReciclado,TipoMaterialReciclable, MaterialAceptado, Publicaciones, Comentarios
from django.utils.timezone import now
from django.utils import timezone
from django.urls import reverse
from core.auth import login_required
from django.db import connection
from django.http import JsonResponse
# usuarios/views.py

from django.contrib import messages
from django.utils.timezone import now


def index(request):
    return render(request, "usuarios/index.html")

def info(request):
    return render(request, "usuarios/infoecoguia.html")


def login(request: HttpRequest):
    if request.method == "GET":
        return render(request, "usuarios/login.html")

    (email, password) = extract_credentials(request)

    # Si el correo y contrasena son correctos, permite el accesso
    (valid, message, user) = verify_crendentials(email, password)

    if not valid:
        return render(
            request, "usuarios/login.html", {"message": message, "email": email}
        )

    # Guarda el id del usuario en la session
    request.session["user_id"] = user.id_usuario

    # Redirecciona a la vista adecuada segun el tipo de usuario
    return map_user_rol(user)

def logout(request: HttpRequest):
    request.session.flush()
    return redirect('usuarios:login')

@login_required(role="usuario")
# def perfil_usuario(request):
#     usuario = get_object_or_404(Usuarios, pk=request.user.id_usuario)
#     modo_edicion = request.GET.get("editar") == "1"

#     if request.method == 'POST':
#         usuario.nombre = request.POST.get('nombre')
#         usuario.ap_paterno = request.POST.get('ap_paterno')
#         usuario.ap_materno = request.POST.get('ap_materno')
#         usuario.correo = request.POST.get('correo')
#         usuario.contrasena = request.POST.get('contrasena')
#         usuario.fecha_nacimiento = request.POST.get('fecha_nacimiento')
#         usuario.save()
#         return redirect('usuarios:perfil_usuario')

#     return render(request, 'usuarios/perfil.html', {
#         'usuario': usuario,
#         'modo_edicion': modo_edicion
#     })

def perfil_usuario(request):
    usuario = get_object_or_404(Usuarios, pk=request.user.id_usuario)
    modo_edicion = request.GET.get("editar") == "1"

    if request.method == 'POST':
        usuario.nombre = request.POST.get('nombre')
        usuario.ap_paterno = request.POST.get('ap_paterno')
        usuario.ap_materno = request.POST.get('ap_materno')
        usuario.correo = request.POST.get('correo')
        usuario.contrasena = request.POST.get('contrasena')
        usuario.fecha_nacimiento = request.POST.get('fecha_nacimiento')
        usuario.save()
        return redirect('usuarios:perfil_usuario')

    # Obtener recompensas del usuario
    recompensas = Recompensas.objects.filter(
        usuariosrecompensas__id_usuario=usuario.id_usuario
    )

    return render(request, 'usuarios/perfil.html', {
        'usuario': usuario,
        'modo_edicion': modo_edicion,
        'recompensas': recompensas
    })

def ranking_usuarios(request):
    usuarios = Usuarios.objects.filter(puntos__isnull=False).order_by('-puntos')[:50]  # top 50
    return render(request, 'usuarios/ranking.html', {'usuarios': usuarios})


def contenido_educativo(request):
    contenidos = ContenidoEducativo.objects.all()
    for contenido in contenidos:
        if contenido.videos:
         contenido.videos_embed = convertir_a_embed(contenido.videos)
    return render(request, 'usuarios/contenido_educativo.html', {'contenidos': contenidos})
# vista para poder utilizar URLS embebidos para insertarlos
def convertir_a_embed(url):
    # if "watch?v=" in url:
    #     return url.replace("watch?v=", "embed/")
    # return url
    import re

    # Extraer ID del video
    video_id = None

    # Caso watch?v=
    m = re.search(r'v=([^\?&]+)', url)
    if m:
        video_id = m.group(1)
    else:
        # Caso youtu.be/
        m = re.search(r'youtu\.be/([^\?&]+)', url)
        if m:
            video_id = m.group(1)

    if video_id:
        return f'https://www.youtube.com/embed/{video_id}'
    else:
        # Si no se puede extraer ID, retorna la URL original
        return url
    
def lista_entregas(request):
    entregas = Entregas.objects.all()
    return render(request, 'usuarios/lista_entregas.html', {'entregas': entregas})  
def confirmar_entrega(request, clave):
    # Obtenemos la entrega
    entrega = get_object_or_404(Entregas, clave=clave)
    entrega.confirmacion = True  # Marcamos como confirmada
    entrega.save()

    # Asignar recompensa al usuario
    usuario = entrega.usuario

    # Por ejemplo: dar la recompensa por "Primera entrega"
    reto, created = Retos.objects.get_or_create(
        titulo="Primera entrega",
        defaults={
            'descripcion': "¡Felicidades por tu primera entrega!",
            'cant_puntos': 100
        }
    )

    Recompensas.objects.create(usuario=usuario, reto=reto)

    # Sumar puntos al usuario
    if usuario.puntos is None:
        usuario.puntos = 0
    usuario.puntos += reto.cant_puntos
    usuario.save()

    return redirect('usuarios:entregas_confirmadas')

# Utilities, not views
# Dependiendo del rol del usuario, redireccionar al area correspondiente
def map_user_rol(user: Usuarios):
    match user.id_rol.pk:  # type: ignore
        # Admin
        case 1:
            return redirect(preserve_request=True, to="administradores:index")
        # Usuario
        case 2:
            return redirect(preserve_request=True, to="usuarios:index")
        # Recicladora
        case 3:
            return redirect(preserve_request=True, to="recicladoras:index")


def extract_credentials(request: HttpRequest) -> tuple[str, str]:
    email = ""
    password = ""
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

    return email, password


# Verifica que el usuario y contrasena sean validos, retorna una tupla que indica si el valor es valido y un mensaje de error, junto con el usuario
def verify_crendentials(email, password) -> tuple[bool, str, Usuarios]:
    db_user = Usuarios.objects.filter(correo=email).first()

    if not db_user:
        return False, "Correo electonico no registrado.", Usuarios()
    elif db_user.contrasena == password:
        return True, "", db_user
    else:
        return False, "Contrasena incorrecta.", Usuarios()
    



def usuariosregistro(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        ap_paterno = request.POST.get("ap_paterno")
        ap_materno = request.POST.get("ap_materno")
        correo = request.POST.get("correo")
        contrasena = request.POST.get("contrasena")
        fecha_nacimiento = request.POST.get("fecha_nacimiento")

        context = {
            "nombre": nombre,
            "ap_paterno": ap_paterno,
            "ap_materno": ap_materno,
            "correo": correo,
            "fecha_nacimiento": fecha_nacimiento,
        }

        # Validar que el correo no exista ya
        if Usuarios.objects.filter(correo=correo).exists():
            context["error_correo"] = "Este correo ya está registrado."
            return render(request, "usuarios/registro.html", context)

        # Aquí puedes añadir más validaciones si quieres

        try:
            Usuarios.objects.create(
                nombre=nombre,
                ap_paterno=ap_paterno,
                ap_materno=ap_materno,
                correo=correo,
                contrasena=contrasena,
                fecha_nacimiento=fecha_nacimiento,
                fecha_registro=now(),
                total_recompensas=0,
                id_rol_id=2,
            )
            return redirect("usuarios:index")
        except Exception as e:
            context["error_general"] = "Error al registrar usuario, intenta de nuevo."
            return render(request, "usuarios/registro.html", context)

    return render(request, "usuarios/registro.html")

def usuarios_delete(request, pk):
    usuarios = get_object_or_404(Usuarios, pk=pk)

    if request.method == "POST":
        usuarios.delete()
        return redirect(reverse('usuarios:index'))

    # Si es GET, renderiza la plantilla de confirmación
    return render(request, "usuarios:usuarios_delete.html", {"object": usuarios})

def mostrarentregas(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect('usuarios:login')  # O la vista que uses para login

    query = """
  select u.nombre,
        e.id_entrega as entrega,
        e.punto_entrega as puntodeentrega,
        emr.id_material as material,
        mr.nombre as nombreMaterial,
        emr.cantidad as cantidad,
        e.fecha_entrega as fecha
        from usuarios u
    JOIN entregas e
    on e.id_usuario_e = u.id_usuario
    JOIN entrega_material_reciclado emr
    ON emr.id_entrega=e.id_entrega
    JOIN material_reciclable mr 
    ON mr.id_material=emr.id_material
    WHERE u.id_usuario= %s
    """

    with connection.cursor() as cursor:
        cursor.execute(query, [user_id])
        rows = cursor.fetchall()

    entregas_dict = {}
    for nombre, entrega_id, punto_entrega, material_id, nombre_material, cantidad, entrega_fecha in rows:

        if entrega_id not in entregas_dict:
            entregas_dict[entrega_id] = {
                'id_entrega': entrega_id,
                'fecha_entrega': entrega_fecha,
                'punto_entrega': punto_entrega,
                'materiales': [],
                'usuario_nombre': nombre,
            }
        entregas_dict[entrega_id]['materiales'].append({
            'id_material': material_id,
            'nombre_material': nombre_material,
            'cantidad': cantidad,
        })

    entregas = list(entregas_dict.values())
     # Consulta retos cumplidos
    query_retos = """
    SELECT u.nombre, r.titulo, r.descripcion,ur.fecha_fin
    FROM usuarios u
    JOIN usuarios_retos ur ON ur.id_usuario = u.id_usuario
    JOIN retos r ON r.codigo = ur.id_reto
    WHERE ur.id_usuario = %s
    ORDER BY ur.fecha_fin DESC
    """

    with connection.cursor() as cursor:
        cursor.execute(query_retos, [user_id])
        rows_retos = cursor.fetchall()

    # Procesamos retos a lista de dicts
    retos = []
    for nombre, titulo, descripcion,fecha_fin in rows_retos:
        retos.append({
            'usuario_nombre': nombre,
            'titulo': titulo,
            'descripcion':descripcion,
            'fecha_fin': fecha_fin,
        })

    return render(request, "usuarios/mostrarentregas.html",{'entregas': entregas, 'retos': retos,
})
    #return render(request, "usuarios/registro.html")
    
def vista_json_recicladoras_con_materiales(request):
    datos = []

    puntos = PuntosReciclaje.objects.all()

    for punto in puntos:
        materiales = MaterialAceptado.objects.filter(id_punto=punto).select_related('id_tipo_material')

        datos.append({
            'id': punto.id_punto,
            'nombre': punto.nombre,
            'ciudad': punto.ciudad,
            'ubicacion': punto.ubicacion,
            'telefono': punto.telefono,
            'materiales': [
                {
                    'id': m.id_tipo_material.id_tmr,
                    'nombre': m.id_tipo_material.nombre,
                    'descripcion': m.id_tipo_material.descripcion,
                    'tiempo_descomposicion': m.id_tipo_material.tiempo_descomposicion,
                    'imagen': m.id_tipo_material.imagen.url if m.id_tipo_material.imagen else None
                }
                for m in materiales
            ]
        })

    return JsonResponse({'puntos_reciclaje': datos})

def vista_html_recicladoras_con_materiales(request):
    puntos = PuntosReciclaje.objects.all()
    contexto = []

    for punto in puntos:
        materiales = MaterialAceptado.objects.filter(id_punto=punto).select_related('id_tipo_material')
        contexto.append({
            'punto': punto,
            'materiales': [m.id_tipo_material for m in materiales]
        })

    return render(request, 'usuarios/recicladoras_materiales.html', {'datos': contexto})

def detalle_punto_reciclaje(request, id_punto):
    punto = get_object_or_404(PuntosReciclaje, id_punto=id_punto)
    materiales = MaterialAceptado.objects.filter(id_punto=punto).select_related('id_tipo_material')

    datos = {
        'id': punto.id_punto,
        'nombre': punto.nombre,
        'ciudad': punto.ciudad,
        'ubicacion': punto.ubicacion,
        'telefono': punto.telefono,
        'descripcion': punto.descripcion,
        'horario_entrada': punto.horario_entrada,
        'horario_salida': punto.horario_salida,
        'materiales': [
            {
                'id': m.id_tipo_material.id_tmr,
                'nombre': m.id_tipo_material.nombre,
                'descripcion': m.id_tipo_material.descripcion,
                'tiempo_descomposicion': m.id_tipo_material.tiempo_descomposicion,
                'imagen': m.id_tipo_material.imagen.url if m.id_tipo_material.imagen else None
            }
            for m in materiales
        ]
    }

    return render(request, 'usuarios/punto_detalle.html', {'punto': datos})
def clasificacion(request):
    clasificacion = TipoMaterialReciclable.objects.all()
    return render(request, "usuarios/clasificacion_materiales.html", {"clasificacion": clasificacion})

###################################################################################
def publicaciones(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect('usuarios:login')
    publicaciones = Publicaciones.objects.all().order_by('-fecha_publicacion')
    context = {
        'publicaciones': publicaciones
    }
    return render(request, 'usuarios/publicaciones.html', context)

def ver_publicaciones(request):
    publicaciones = Publicaciones.objects.all().order_by('-fecha_publicacion')
    usuario_actual = request.user 
    return render(request, 'tu_app/publicaciones.html', {
        'publicaciones': publicaciones,
        'usuario_actual': usuario_actual,
    })
def crear_comentario(request):
    if request.method == "POST":
        post_id = request.POST.get('post_id')
        contenido = request.POST.get('contenido')
        user_id = request.session.get("user_id")

        if post_id and contenido and user_id:
            publicacion = get_object_or_404(Publicaciones, clave_publicacion=post_id)
            usuario = get_object_or_404(Usuarios, id_usuario=user_id)

            Comentarios.objects.create(
                id_publicacion=publicacion,
                id_usuario=usuario,
                contenido=contenido,
                fecha_creacion=timezone.now()
            )

    return redirect('usuarios:publicaciones')

def crear_publicacion(request):
    if request.method == "POST":
        titulo = request.POST.get("titulo")
        contenido = request.POST.get("contenido")

        if titulo or contenido:
            Publicaciones.objects.create(
                titulo=titulo,
                contenido=contenido,
                id_usuario_p=request.user,
                fecha_publicacion=timezone.now()
            )

        return redirect('usuarios:publicaciones')

    return redirect('usuarios:publicaciones')
##############################################################################