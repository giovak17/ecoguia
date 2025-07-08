from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
import traceback
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

def solicitud_registro_view(request):
    if request.method == 'POST':
        form = SolicitudRegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registro_exitoso')  # redirige a una vista de éxito
    else:
        form = SolicitudRegistroForm()
    return render(request, 'recicladoras/solicitud_registro.html', {'form': form})

def agregar_punto(request):
    if request.method == "POST":
        try:
            nombre = request.POST.get("nombre")
            ubicacion = request.POST.get("ubicacion")
            ciudad = request.POST.get("ciudad")
            horario_entrada = request.POST.get("horario_entrada")
            horario_salida = request.POST.get("horario_salida")
            latitud = request.POST.get("latitud")
            longitud = request.POST.get("longitud")

            PuntosReciclaje.objects.create(
                nombre=nombre,
                ubicacion=ubicacion,
                ciudad=ciudad,
                horario_entrada=horario_entrada,
                horario_salida=horario_salida,
                latitud=latitud,
                longitud=longitud,
                id_recicladora=Recicladoras.objects.get(pk=1)
            )

            print("Punto insertado con éxito.")
            return redirect("recicladoras:index")

        except Exception as e:
            print("Error al insertar:")
            traceback.print_exc()
            return redirect("recicladoras:agregar_punto")

    return render(request, "recicladoras/agregar_punto.html")


