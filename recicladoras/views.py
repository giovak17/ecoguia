import os
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, redirect
import traceback
from core.models import Entregas, Recicladoras, PuntosReciclaje, EntregaMaterialReciclado, TipoMaterialReciclable, Usuarios, MaterialAceptado, MaterialReciclable
from core.auth import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse

# Create your views here.

@login_required(role="recicladora")
def index(request):
    return render(request, "recicladoras/index.html")

@login_required(role="recicladora")
# def confirmar_entregas(request):
#     user_id = request.user.id_usuario
#     success = False

#     if request.method == 'POST':
#         for key, value in request.POST.items():
#             if key.startswith('confirmada_'):
#                 entrega_id = key.split('_')[1]
#                 try:
#                     entrega = Entregas.objects.get(pk=entrega_id)
#                     if entrega.punto_entrega and entrega.punto_entrega.id_recicladora.propietario.id_usuario == user_id:
#                         entrega.confirmada = True if value == 'true' else False
#                         entrega.save()
#                 except Entregas.DoesNotExist:
#                     continue
#         success = True

#     entregas_queryset = Entregas.objects.select_related(
#         'id_usuario_e',
#         'punto_entrega',
#         'punto_entrega__id_recicladora'
#     ).filter(
#         punto_entrega__id_recicladora__propietario__id_usuario=user_id
#     )

#     entregas = []
#     for entrega in entregas_queryset:
#         materiales_entregados = EntregaMaterialReciclado.objects.filter(id_entrega=entrega).select_related('id_material')

#         materiales = [
#             {
#                 'nombre': m.id_material.nombre,
#                 'cantidad': m.cantidad,
#                 'condiciones': m.condiciones_entrega
#             }
#             for m in materiales_entregados
#         ]

#         entregas.append({
#             'entrega': entrega,
#             'correo': entrega.id_usuario_e.correo,
#             'materiales': materiales
#         })

#     return render(request, 'recicladoras/confirmar_entregas.html', {
#         'entregas': entregas,
#         'success': success
#     })

def confirmar_entregas(request):
    try:
        recicladora = Recicladoras.objects.get(propietario_id=request.user.id_usuario)
    except Recicladoras.DoesNotExist:
        messages.error(request, "No tienes una recicladora asociada.")
        return redirect('recicladoras:index')

    puntos = PuntosReciclaje.objects.filter(id_recicladora=recicladora.codigo_recicladora)

    if request.method == 'POST':
        correo = request.POST.get('correo')
        punto_entrega_id = request.POST.get('punto_entrega')

        materiales_ids = request.POST.getlist('material[]')
        cantidades = request.POST.getlist('cantidad[]')
        condiciones_list = request.POST.getlist('condiciones[]')

        if not puntos.filter(id_punto=punto_entrega_id).exists():
            messages.error(request, "Punto inválido.")
            return redirect('recicladoras:confirmar_entregas')

        try:
            usuario = Usuarios.objects.get(correo=correo)
        except Usuarios.DoesNotExist:
            messages.error(request, "Correo no encontrado.")
            return redirect('recicladoras:confirmar_entregas')

        # Crear una sola entrega
        entrega = Entregas.objects.create(
            fecha_entrega=timezone.now(),
            id_usuario_e=usuario,
            punto_entrega_id=punto_entrega_id,
            confirmada=False
        )

        # Iterar sobre cada material y registrar
        for i in range(len(materiales_ids)):
            EntregaMaterialReciclado.objects.create(
                id_entrega=entrega,
                id_material_id=materiales_ids[i],
                cantidad=cantidades[i],
                condiciones_entrega=condiciones_list[i]
            )

        messages.success(request, "Entrega registrada correctamente.")
        return redirect('recicladoras:confirmar_entregas')

    return render(request, 'recicladoras/confirmar_entregas.html', {
        'puntos': puntos
    })




def get_materiales_aceptados(request, punto_id):
    materiales_ids = MaterialAceptado.objects.filter(id_punto=punto_id).values_list('id_tipo_material', flat=True)
    materiales = MaterialReciclable.objects.filter(tipo_reciclaje_id__in=materiales_ids)

    data = [{'id': m.id_material, 'nombre': m.nombre} for m in materiales]
    return JsonResponse(data, safe=False)




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
    user_id = request.session.get("user_id")

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        ubicacion = request.POST.get('ubicacion')
        telefono = request.POST.get('telefono')
        horario_entrada = request.POST.get('horario_entrada')
        horario_salida = request.POST.get('horario_salida')
        
        # --- Campo 'ciudad' AGREGADO y capturado ---
        ciudad = request.POST.get('ciudad')
        
        descripcion = request.POST.get('descripcion')
        extras = request.POST.get('extras')
        
        # Conversión de latitud y longitud a float (esencial para FloatField)
        latitud_str = request.POST.get('latitud')
        longitud_str = request.POST.get('longitud')

        latitud = None
        longitud = None

        if latitud_str:
            try:
                latitud = float(latitud_str)
            except ValueError:
                # Si el valor no es un número válido, se quedará como None
                pass 
        
        if longitud_str:
            try:
                longitud = float(longitud_str)
            except ValueError:
                # Si el valor no es un número válido, se quedará como None
                pass

        recicladora_codigo = request.POST.get('id_recicladora')
        
        # --- Obtener IDs de materiales seleccionados del formulario ---
        # request.POST.getlist() es para campos de selección múltiple
        materiales_seleccionados_ids = request.POST.getlist('materiales_aceptados') 

        try:
            # Obtener el objeto Recicladora
            recicladora = get_object_or_404(Recicladoras, codigo_recicladora=recicladora_codigo)

            # Crear y guardar el nuevo PuntosReciclaje
            punto = PuntosReciclaje(
                nombre=nombre,
                ubicacion=ubicacion,
                telefono=telefono,
                horario_entrada=horario_entrada,
                horario_salida=horario_salida,
                ciudad=ciudad,  # <-- Campo 'ciudad' asignado
                descripcion=descripcion,
                id_recicladora=recicladora,
                extras=extras,
                latitud=latitud,
                longitud=longitud
            )
            punto.save() # Es crucial guardar el punto primero para obtener su id_punto

            # --- Insertar los materiales aceptados en la tabla MaterialAceptado ---
            if materiales_seleccionados_ids:
                for material_id in materiales_seleccionados_ids:
                    try:
                        # Recuperar el objeto TipoMaterialReciclable usando su PK (id_tmr)
                        tipo_material = get_object_or_404(TipoMaterialReciclable, id_tmr=material_id)
                        
                        # Crear la relación en MaterialAceptado
                        MaterialAceptado.objects.create(
                            id_punto=punto, # Usa el objeto PuntosReciclaje recién creado
                            id_tipo_material=tipo_material # Usa el objeto TipoMaterialReciclable
                        )
                    except TipoMaterialReciclable.DoesNotExist:
                        # Esto podría ocurrir si un ID de material no existe en la BD
                        pass # No se loguea ni muestra mensaje según lo solicitado
                    except Exception as e:
                        # Otros errores al asociar el material
                        pass # No se loguea ni muestra mensaje según lo solicitado

            return redirect('recicladoras:index') 

        except Recicladoras.DoesNotExist:
            pass # No se loguea ni muestra mensaje según lo solicitado
        except Exception as e:
            pass # No se loguea ni muestra mensaje según lo solicitado

    # Para peticiones GET o si hubo algún problema en POST (sin redirigir)
    recicladoras = Recicladoras.objects.filter(propietario=user_id)
    # Obtener todos los tipos de materiales para mostrarlos en el select del formulario
    tipos_materiales = TipoMaterialReciclable.objects.all() 

    context = {
        'recicladoras': recicladoras,
        'tipos_materiales': tipos_materiales, # Pasa la lista de materiales al contexto
    }
    return render(request, 'recicladoras/agregar_punto.html', context)


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
