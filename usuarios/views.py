from django.http import HttpRequest
from django.shortcuts import redirect, render
from core.models import Usuarios,Entregas


def index(request):
    return render(request, "usuarios/index.html")

def login(request: HttpRequest): 
    if request.method == "GET":
        return render(request, "usuarios/login.html")

    email = request.POST["email"]
    password = request.POST["password"]

    user = Usuarios.objects.filter(correo_electronico=email).first()

    # Si el correo y contrasena son correctos, permite el accesso
    if user and user.contrasena == password:
        return redirect("usuarios:index")
    
    if not user:
        message = "Correo electronico no registrado."
    else:
        if user.contrasena != password: 
            message = "Contrasena incorrecta."


    return render(request, "usuarios/login.html", {"message": message, "email": email})


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

