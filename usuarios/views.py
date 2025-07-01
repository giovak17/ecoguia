from django.shortcuts import render
# from core.models import Usuarios


def index(request):
    return render(request, "usuarios/index.html")
