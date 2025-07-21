from django.http import HttpRequest
<<<<<<< HEAD
=======
from django.shortcuts import redirect, render, get_object_or_404
from core.models import Usuarios,Entregas
>>>>>>> 1e94b3394d24dae885092b94f9c4644951ffeef8
from django.shortcuts import redirect, render
from core.models import Usuarios,Entregas, PuntosReciclaje
from django.utils.timezone import now
from django.http import JsonResponse
from django.db import connection
from django.urls import reverse

def index(request):
    return render(request, "usuarios/index.html")


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

def contenido_educativo(request):

    contenidos = [
        {
            'titulo': 'Cómo separar residuos correctamente',
            'descripcion': 'Guía visual para separar papel, plástico, vidrio y orgánicos.',
            'tipo': 'imagen',
            'archivo': 'contenido/contenedores.webp',
            'fecha': '2025-07-05'
        },
        {       
            'titulo': 'Video: El impacto del reciclaje en el planeta',
            'descripcion': 'Un breve documental sobre cómo el reciclaje ayuda al medio ambiente.',
            'tipo': 'youtube',
            'archivo': convertir_a_embed("https://www.youtube.com/watch?v=cvakvfXj0KE"),
            'fecha': '2025-06-28'
        },
        {
            'titulo': 'Infografía: ¿Qué puedo reciclar?',
            'descripcion': 'Infografía sobre materiales que sí y no se pueden reciclar.',
            'tipo': 'imagen',
            'archivo': 'contenido/recicla.jpeg',
            'fecha': '2025-06-15'
        }
    ]
    return render(request, 'usuarios/contenido_educativo.html', {'contenidos': contenidos})

def convertir_a_embed(url):
    if "watch?v=" in url:
        return url.replace("watch?v=", "embed/")
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
    
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.timezone import now


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


def mapa_puntos_google(request):
    puntos = list(PuntosReciclaje.objects.values(
        'nombre', 'latitud', 'longitud', 'ubicacion', 'ciudad'
    ))
    return render(request, 'usuarios/mapa_google.html', {'puntos': puntos})

def usuarios_delete(request, pk):
    usuarios = get_object_or_404(Usuarios, pk=pk)

    if request.method == "POST":
        usuarios.delete()
        return redirect(reverse('usuarios:index'))

    # Si es GET, renderiza la plantilla de confirmación
    return render(request, "usuarios:usuarios_delete.html", {"object": usuarios})