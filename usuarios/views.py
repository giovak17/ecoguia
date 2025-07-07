from django.http import HttpRequest
from django.shortcuts import redirect, render
from core.models import Usuarios


def index(request):
    return render(request, "usuarios/index.html")

def login(request: HttpRequest): 
    if request.method == "GET":
        return render(request, "usuarios/login.html")

    email = request.POST["email"]
    password = request.POST["password"]

    user = Usuarios.objects.filter(correo=email).first()

    # Si el correo y contrasena son correctos, permite el accesso
    if user and user.contrasena == password:
        return redirect("usuarios:index")
    
    if not user:
        message = "Correo electronico no registrado."
    else:
        if user.contrasena != password: 
            message = "Contrasena incorrecta."


    return render(request, "usuarios/login.html", {"message": message, "email": email})




