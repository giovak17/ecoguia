from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from core.models import Entregas, Recicladoras, PuntosReciclaje, EntregaMaterialReciclado


# Create your views here.
def index(request):
    return render(request, "recicladoras/index.html")

# En progreso
def confirmar_entregas(request: HttpRequest):
    user_id = int(request.session["user_id"])

    print(request.session["user_id"])
    return HttpResponse(request.session["user_id"] )

    # return render(request, "recicladoras/confirmar_entregas.html")


