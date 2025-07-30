import os
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, redirect
import traceback
from core.models import Entregas, Recicladoras, PuntosReciclaje, EntregaMaterialReciclado, TipoMaterialReciclable, Usuarios
from core.auth import login_required

# Create your views here.

@login_required(role="recicladora")
def index(request):
    return render(request, "recicladoras/index.html")

@login_required(role="recicladora")
def confirmar_entregas(request):
    user_id = request.user.id_usuario
    success = False

    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('confirmada_'):
                entrega_id = key.split('_')[1]
                try:
                    entrega = Entregas.objects.get(pk=entrega_id)
                    if entrega.punto_entrega and entrega.punto_entrega.id_recicladora.propietario.id_usuario == user_id:
                        entrega.confirmada = True if value == 'true' else False
                        entrega.save()
                except Entregas.DoesNotExist:
                    continue
        success = True

    entregas_queryset = Entregas.objects.select_related(
        'id_usuario_e',
        'punto_entrega',
        'punto_entrega__id_recicladora'
    ).filter(
        punto_entrega__id_recicladora__propietario__id_usuario=user_id
    )

    entregas = []
    for entrega in entregas_queryset:
        materiales_entregados = EntregaMaterialReciclado.objects.filter(id_entrega=entrega).select_related('id_material')

        materiales = [
            {
                'nombre': m.id_material.nombre,
                'cantidad': m.cantidad,
                'condiciones': m.condiciones_entrega
            }
            for m in materiales_entregados
        ]

        entregas.append({
            'entrega': entrega,
            'correo': entrega.id_usuario_e.correo,
            'materiales': materiales
        })

    return render(request, 'recicladoras/confirmar_entregas.html', {
        'entregas': entregas,
        'success': success
    })



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

def  agregar_punto(request):
    user_id = request.session.get("user_id")

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        ubicacion = request.POST.get('ubicacion')
        telefono = request.POST.get('telefono')
        horario_entrada = request.POST.get('horario_entrada')
        horario_salida = request.POST.get('horario_salida')
        descripcion = request.POST.get('descripcion')
        recicladora_codigo = request.POST.get('id_recicladora')
        extras=request.POST.get('extras')
        latitud =request.POST.get('latitud')
        longitud= request.POST.get('longitud')
        recicladora = Recicladoras.objects.get(codigo_recicladora=recicladora_codigo)

        punto = PuntosReciclaje(
            nombre=nombre,
            ubicacion=ubicacion,
            telefono=telefono,
            horario_entrada=horario_entrada,
            horario_salida=horario_salida,
            descripcion=descripcion,
            id_recicladora=recicladora,
            extras=extras,
            latitud=latitud,
            longitud=longitud
        )
        punto.save()
        
        return redirect('recicladoras:index')  
    # Consulta para llenar el select:
    recicladoras = Recicladoras.objects.filter(propietario=user_id)
    return render(request, 'recicladoras/agregar_punto.html', {'recicladoras': recicladoras})




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



@login_required(role="recicladora")
def verpuntosreciclaje(request):
     user_id = request.session.get("user_id")
     puntos = PuntosReciclaje.objects.select_related('id_recicladora__propietario')\
        .filter(id_recicladora__propietario__id_usuario=user_id)

     context = {
        'puntos': puntos,
    }
     return render(request, "recicladoras/verpuntosreciclaje.html",context)
