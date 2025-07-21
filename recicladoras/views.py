from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, redirect
import traceback
from core.models import Entregas, Recicladoras, PuntosReciclaje, EntregaMaterialReciclado, TipoMaterialReciclable, Usuarios
from .forms import TipoMaterialReciclableForm, SolicitudRegistro
from django.views import generic
from django.urls import reverse, reverse_lazy
from core.models import Entregas, Recicladoras, PuntosReciclaje, EntregaMaterialReciclado
from .forms import SolicitudRecicladoraForm


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
        #form = SolicitudRegistroForm(request.POST)
        form = SolicitudRecicladoraForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registro_exitoso')  # redirige a una vista de éxito
    else:
        #form = SolicitudRegistroForm()
        form = SolicitudRecicladoraForm()
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

def solicitar_recicladora(request):
    if request.method == 'POST':
        form = SolicitudRecicladoraForm(request.POST)
        if form.is_valid():
            recicladora = form.save(commit=False)
            recicladora.aprobada = False  # queda pendiente
            recicladora.save()
            return redirect('solicitud_exitosa')
    else:
        form = SolicitudRecicladoraForm()
    return render(request, 'recicladoras/solicitud_registro.html', {'form': form})

def solicitud_exitosa(request):
    return render(request, 'recicladoras/solicitud_registro.html')

# Listar todos los tipos de material
def tipo_material_list(request):
    tipos_material = TipoMaterialReciclable.objects.all()
    return render(request, "recicladoras/tipomaterial_list.html", {"tipos_material": tipos_material})

def tipo_material_registro(request):
    if request.method == "POST":
        try:
            nombre = request.POST.get("nombre")
            descripcion = request.POST.get("descripcion")
            tiempo_descomposicion = request.POST.get("tiempo")
            
            TipoMaterialReciclable.objects.create(
                nombre=nombre,
                descripcion = descripcion,
                tiempo_descomposicion = tiempo_descomposicion,
            )

            print("Fitro insertado con éxito.")
            return redirect("recicladoras:index")

        except Exception as e:
            print("Error al insertar:")
            traceback.print_exc()
            return redirect("recicladoras:tipomaterial_registro")

    return render(request, "recicladoras/tipomaterial_registro.html")

# Actualizar un tipo de material existente
def tipo_material_update(request, pk):
    tipo_material = get_object_or_404(TipoMaterialReciclable, pk=pk)
    if request.method == "POST":
        form = TipoMaterialReciclableForm(request.POST, instance=tipo_material)
        if form.is_valid():
            form.save()
            return redirect(reverse('tipomaterial_list'))
        else:
            print("Formulario inválido:", form.errors)
    else:
        form = TipoMaterialReciclableForm(instance=tipo_material)
    return render(request, "recicladoras/tipomaterial_registro.html", {"form": form})


def tipo_material_delete(request, pk):
    tipo_material = get_object_or_404(TipoMaterialReciclable, pk=pk)

    if request.method == "POST":
        tipo_material.delete()
        return redirect(reverse('tipomaterial_list'))

    # Si es GET, renderiza la plantilla de confirmación
    return render(request, "tipomaterial_delete.html", {"object": tipo_material})
