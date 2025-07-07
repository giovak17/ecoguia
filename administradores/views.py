from django.shortcuts import render
from core.models import Recicladoras

# Create your views here.
def index(request):
    return render(request, "administradores/index.html")
def ver_recicladoras(request):
    recicladoras = Recicladoras.objects.select_related('propietario').all()
    return render(request, 'administradores/recicladoras.html', {'recicladoras': recicladoras})
