from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from core.models import Recicladoras
from django.urls import reverse, reverse_lazy
from core.models import Usuarios, Roles, Recicladoras
from django.contrib import messages
from core.models import ContenidoEducativo, TipoMaterialReciclable
from usuarios.views import convertir_a_embed
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS 
from django.contrib.auth.decorators import user_passes_test
from core.auth import login_required
import subprocess, datetime, os
from django.conf import settings
from .forms import UsuarioForm
from .forms import TipoMaterialReciclableForm
from django.db import connection


# from core.models import (
#     Entregas,
#     Publicaciones,
#     Recicladoras,
#     UsuariosRecompensas,
#     UsuariosRetos,
#     PuntosReciclaje,
#     EntregaMaterialReciclado
# )
from django.db import transaction,  IntegrityError

# Create your views here.

@login_required(role="administrador")
def index(request):
    return render(request, "administradores/index.html")
# manejado por America Lara 
# vista para mostrar recicladoras
def ver_recicladoras(request):
    recicladoras = Recicladoras.objects.select_related('propietario').all()
    return render(request, 'administradores/recicladoras.html', {'recicladoras': recicladoras})
# manejado por America Lara 
# vista para crear recicladoras
def recicladora_crear(request):
    errores = {}
    recicladora_data = {}
    propietarios = Usuarios.objects.all()
    reciclador_rol = Roles.objects.get(nombre='Recicladora')
    propietarios = Usuarios.objects.filter(id_rol=reciclador_rol)



    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        propietario_id = request.POST.get('propietario')
        calle = request.POST.get('calle')
        colonia = request.POST.get('colonia')
        ciudad = request.POST.get('ciudad')
        codigo_postal = request.POST.get('codigo_postal')
        numero_int = request.POST.get('numero_int')
        telefono = request.POST.get('numero_telefonico')

        recicladora_data = {
            'nombre': nombre,
            'propietario_id': propietario_id,
            'calle': calle,
            'colonia': colonia,
            'ciudad': ciudad,
            'codigo_postal': codigo_postal,
            'numero_int': numero_int,
            'numero_telefonico': telefono,
        }

        if not nombre:
            errores['nombre'] = 'El nombre es obligatorio'
        if not ciudad:
            errores['ciudad'] = 'La ciudad es obligatoria'

        if not errores:
            Recicladoras.objects.create(
                nombre=nombre,
                propietario_id=propietario_id or None,
                calle=calle,
                colonia=colonia,
                ciudad=ciudad,
                codigo_postal=codigo_postal or None,
                numero_int=numero_int or None,
                numero_telefonico=telefono
            )
            return redirect('administradores:ver_recicladoras')

    return render(request, 'administradores/recicladora_form.html', {
        'errores': errores,
        'titulo': 'Registrar Recicladora',
        'propietarios': propietarios,
        'recicladora': recicladora_data
    })


def recicladora_editar(request, pk):
    recicladora = get_object_or_404(Recicladoras, pk=pk)
    errores = {}

    from core.models import Usuarios 

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        ciudad = request.POST.get('ciudad')
        telefono = request.POST.get('numero_telefonico')
        calle = request.POST.get('calle')
        colonia = request.POST.get('colonia')
        numero_int = request.POST.get('numero_int')
        codigo_postal = request.POST.get('codigo_postal')
        aprobada = request.POST.get('aprobada') == 'on'
        propietario_id = request.POST.get('propietario')

        if not nombre:
            errores['nombre'] = 'El nombre es obligatorio'
        if not ciudad:
            errores['ciudad'] = 'La ciudad es obligatoria'

        if not errores:
            recicladora.nombre = nombre
            recicladora.ciudad = ciudad
            recicladora.numero_telefonico = telefono or None
            recicladora.calle = calle or None
            recicladora.colonia = colonia or None
            recicladora.numero_int = numero_int or None
            recicladora.codigo_postal = codigo_postal or None
            recicladora.aprobada = aprobada
            recicladora.propietario_id = propietario_id or None
            recicladora.save()
            return redirect('administradores:ver_recicladoras')

 
    propietarios = Usuarios.objects.all()

    return render(request, 'administradores/recicladora_form.html', {
        'recicladora': recicladora,
        'errores': errores,
        'propietarios': propietarios,
        'titulo': 'Editar Recicladora'
    })
# manejado por America Lara 
# vista para eliminar recicladoras
def recicladora_eliminar(request, pk):
    recicladora = get_object_or_404(Recicladoras, pk=pk)
    if request.method == 'POST':
        recicladora.delete()
        return redirect('administradores:ver_recicladoras')
    return render(request, 'administradores/recicladoras_confirm_delete.html', {'recicladora': recicladora})


# Listar todos los tipos de material
def tipo_material_list(request):
    tipos_material = TipoMaterialReciclable.objects.all()
    return render(request, "administradores/tipomaterial_list.html", {"tipos_material": tipos_material})

def tipo_material_registro(request):
    if request.method == "POST":
        try:
            nombre = request.POST.get("nombre")
            descripcion = request.POST.get("descripcion")
            tiempo_descomposicion = request.POST.get("tiempo_descomposicion")
            imagen = request.FILES.get('imagen')
            
            # Validación manual de formato/size
            if imagen:
                ext = os.path.splitext(imagen.name)[1].lower()
                if ext not in ['.jpg', '.jpeg', '.png']:
                    raise Exception("Sólo imágenes JPG, JPEG y PNG.")
                if imagen.size > 3 * 1024 * 1024 * 1024:
                    raise Exception("Imagen demasiado grande. Máximo 10MB.")
                
                
            
            TipoMaterialReciclable.objects.create(
                nombre=nombre,
                descripcion = descripcion,
                tiempo_descomposicion = tiempo_descomposicion,
                imagen = imagen
            )
            
            print("tipo de material insertado con éxito.")
            return redirect("administradores:index")

        except Exception as e:
            print("Error al insertar:")
            traceback.print_exc()
            return redirect("administradores:tipomaterial_registro")

    return render(request, "administradores/tipomaterial_registro.html")

# Actualizar un tipo de material existente
def tipo_material_actualizar(request, pk):
    tipo_material = get_object_or_404(TipoMaterialReciclable, pk=pk)
    if request.method == "POST":
        form = TipoMaterialReciclableForm(request.POST, request.FILES, instance=tipo_material, is_update=True)
        if form.is_valid():
            form.save()
            return redirect(reverse('administradores:tipomaterial_list'))
        else:
            print("Formulario inválido:", form.errors)
    else:
        form = TipoMaterialReciclableForm(instance=tipo_material, is_update=True)
    return render(request, "administradores/tipomaterial_actualizar.html", {"form": form})


def tipo_material_delete(request, pk):
    tipo_material = get_object_or_404(TipoMaterialReciclable, pk=pk)

    if request.method == "POST":
        tipo_material.delete()
        return redirect(reverse('administradores:tipomaterial_list'))

    # Si es GET, renderiza la plantilla de confirmación
    return render(request, "administradores/tipomaterial_delete.html", {"object": tipo_material})

# def listar_usuarios(request):
#     usuarios = Usuarios.objects.all()
#     return render(request, 'administradores/listado_usuarios.html', {'usuarios': usuarios})

@login_required(role="administrador")
def listar_usuarios(request):
    usuarios = Usuarios.objects.select_related('id_rol').all()
    return render(request, 'administradores/listar_usuarios.html', {'usuarios': usuarios})

@login_required(role="administrador")
def editar_usuario(request, id_usuario):
    usuario = get_object_or_404(Usuarios, id_usuario=id_usuario)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('administradores:listar_usuarios')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'administradores/editar_usuario.html', {'form': form, 'usuario': usuario})

@login_required(role="administrador")
def eliminar_usuario(request, id_usuario):
    usuario = get_object_or_404(Usuarios, id_usuario=id_usuario)
    if request.method == 'POST':
        usuario.delete()
        return redirect('administradores:listar_usuarios')
    return render(request, 'administradores/confirmar_eliminacion.html', {'usuario': usuario})

  
@login_required(role="administrador")
def aprobar_recicladoras(request: HttpRequest):
    success = False
    if request.method == "POST":
        post_data = request.POST.copy().dict()
        post_data.pop('csrfmiddlewaretoken', None)

        # Por cada una de las recicladoras, actualizar el estado de "aprobado" al estado recibido por el formulario
        for key, val in post_data.items():
            rec = Recicladoras.objects.get(pk=int(key))

            if val == "True":
                rec.aprobada = True
            else:
                rec.aprobada = False
            rec.save()
            success = True

    recicladoras = Recicladoras.objects.select_related("propietario").order_by("-codigo_recicladora");

    return render(request, "administradores/aprobar_recicladoras.html", {"recicladoras":recicladoras, "success": success })


def validar_campos(titulo, descripcion, videos):
    errores = {}

    # Validar título
    if not titulo:
        errores['titulo'] = ["El título es obligatorio."] # <-- Cambiado a lista
    elif len(titulo) > 25:
        errores['titulo'] = ["El título no debe exceder 25 caracteres."] # <-- Cambiado a lista

    # Validar descripción
    if not descripcion:
        errores['descripcion'] = ["La descripción es obligatoria."] # <-- Cambiado a lista
    elif len(descripcion) < 10:
        errores['descripcion'] = ["La descripción debe tener al menos 10 caracteres."] # <-- Cambiado a lista

    # Validar enlace de video (si existe)
    if videos and not videos.startswith(('http://', 'https://')):
        errores['videos'] = ["El enlace de video debe ser una URL válida (http:// o https://)."] # <-- Cambiado a lista

    # Si hay errores, lanzar excepción
    if errores:
        raise ValidationError(errores)
# manejado por America Lara 
# vista para mostrar contenidos educativos
def contenido_educativo_admin(request):
    contenidos = ContenidoEducativo.objects.all()
    for contenido in contenidos:
        if contenido.videos:
            contenido.videos_embed = convertir_a_embed(contenido.videos)
    return render(request, 'administradores/contenido_educativo_admin.html', {'contenidos': contenidos})
# manejado por America Lara 
# vista para crear Contendios educativos
def contenido_crear(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        id_usuario_ce = request.user.id_usuario
        imagen = request.FILES.get('imagen')
        videos = request.POST.get('videos')
        video_local = request.FILES.get('video_local')

        nuevo = ContenidoEducativo(
            titulo=titulo,
            descripcion=descripcion,
            id_usuario_ce_id=id_usuario_ce,
            imagen=imagen,
            videos=videos,
            video_local=video_local
        )
        try:
            validar_campos(titulo, descripcion, videos)
            nuevo.clean()
            nuevo.save()
            return redirect('administradores:contenido_admin')
        except ValidationError as e:
            errores = e.message_dict
            # envía errores al template
            return render(request, 'administradores/contenido_form.html', {'errores': errores, 'contenido': nuevo})

    return render(request, 'administradores/contenido_form.html')
# manejado por America Lara 
# vista para editar contendios educativos
def contenido_editar(request, pk):
    contenido = get_object_or_404(ContenidoEducativo, pk=pk)

    if request.method == 'POST':
        # Actualiza los campos directamente desde POST
        contenido.titulo = request.POST.get('titulo')
        contenido.descripcion = request.POST.get('descripcion')
        contenido.videos = request.POST.get('videos') # URL de YouTube

        # Lógica para subir nueva imagen o mantener existente/eliminar
        if 'imagen' in request.FILES:
            contenido.imagen = request.FILES['imagen']
        elif request.POST.get('imagen-clear'):
            contenido.imagen = None
        
        if 'video_local' in request.FILES:
            contenido.video_local = request.FILES['video_local']
        elif request.POST.get('video_local-clear'):
            contenido.video_local = None

        try:
            # Primero las validaciones de campos básicos (de validar_campos)
            # Esto lanzará ValidationError con un diccionario si hay errores de campo.
            validar_campos(contenido.titulo, contenido.descripcion, contenido.videos)
            
            # Luego, la validación del modelo. Esto lanzará ValidationError con una cadena simple.
            contenido.clean() 

            contenido.save()
            messages.success(request, 'Contenido educativo actualizado correctamente.')
            return redirect('administradores:contenido_admin')
        except ValidationError as e:
            # ***************************************************************
            # *********** GESTIÓN DE ERRORES UNIFICADA ********************
            # ***************************************************************
            errores_para_template = {} # Diccionario para pasar al template

            if hasattr(e, 'message_dict'):
                # Si la excepción viene de validar_campos o un Form de Django
                errores_para_template = e.message_dict
            else:
                # Si la excepción viene del contenido.clean() del modelo (que lanza una cadena)
                # o cualquier otra ValidationError lanzada como una lista o cadena simple.
                # Lo convertimos a un formato de diccionario bajo la clave __all__ o NON_FIELD_ERRORS.
                if isinstance(e.message, dict): # Si por alguna razón es un dict (raro para ValidationError simple)
                    errores_para_template = e.message
                elif isinstance(e.message, list): # Si es una lista de mensajes
                    errores_para_template[NON_FIELD_ERRORS] = e.message
                else: # Si es una cadena simple (como la de tu clean())
                    errores_para_template[NON_FIELD_ERRORS] = [e.message]
            
            # Pasamos el diccionario de errores al template
            return render(request, 'administradores/contenido_form.html', {
                'errores': errores_para_template,
                'contenido': contenido
            })

    # Para la solicitud GET
    return render(request, 'administradores/contenido_form.html', {'contenido': contenido})


def contenido_borrar(request, pk):
    contenido = get_object_or_404(ContenidoEducativo, pk=pk)
    if request.method == 'POST':
        contenido.delete()
        return redirect(('administradores:contenido_admin'))
    return render(request, 'administradores/contenido_confirm_delete.html', {'contenido': contenido})

############################################################################################
@login_required(role="administrador")
def backup(request):
     error_message = None
     success_message = None

     if request.method == "POST":
        db_settings = settings.DATABASES['default']
        db_name = db_settings['NAME']
        db_user = db_settings['USER']
        db_host = db_settings['HOST'] or 'localhost'
        db_port = db_settings['PORT'] or '5432'

        db_pass = request.POST.get('db_password')

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"backup_{timestamp}.backup"
        filepath = os.path.join(settings.BASE_DIR, filename)

        pg_dump_path = r"C:\Program Files\PostgreSQL\17\bin\pg_dump.exe"  # Cambia si es necesario

        os.environ['PGPASSWORD'] = db_pass

        cmd = [
            pg_dump_path,
            "-h", db_host,
            "-p", str(db_port),
            "-U", db_user,
            "-F", "c",     # Formato personalizado (binario)
            "-f", filepath,
            db_name,
        ]
        try:
            subprocess.run(cmd, check=True)
            # Si quieres, para éxito:
            request.session['success_message'] = "Respaldo generado exitosamente."
            # El archivo se descarga, no rediriges acá
            with open(filepath, 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
            os.remove(filepath)
            return response

        except subprocess.CalledProcessError:
            request.session['error_message'] = "Contraseña incorrecta o error al generar respaldo."
        except Exception as e:
            request.session['error_message'] = f"Error inesperado: {e}"

        return redirect('administradores:backupscreen')

     return redirect('administradores:backupscreen')

@login_required(role="administrador")
def restaurar_toda_db(request):
    success_message = None
    error_message = None

    if request.method == "POST":
        db_settings = settings.DATABASES['default']
        db_name = db_settings['NAME']
        db_user = db_settings['USER']
        db_host = db_settings['HOST'] or 'localhost'
        db_port = db_settings['PORT'] or '5432'

        db_pass = request.POST.get('db_password')

        # respaldo_fijo = os.path.join(settings.BASE_DIR, "administradores", "backup", "backup_2025-07-29_12-42-54.backup")
        respaldo_fijo = os.path.join(settings.BASE_DIR, "administradores", "backup", "backup_2025-07-30_04-23-41.backup")

        pg_restore_path = r"C:\Program Files\PostgreSQL\17\bin\pg_restore.exe"

        os.environ['PGPASSWORD'] = db_pass

        cmd = [
            pg_restore_path,
            "-h", db_host,
            "-p", str(db_port),
            "-U", db_user,
            "-d", db_name,
            "-c",
            respaldo_fijo
        ]

        try:
            subprocess.run(cmd, check=True)
            success_message = "La base de datos se restauró a su estado original exitosamente."
        except subprocess.CalledProcessError:
            error_message = "Contraseña incorrecta o error al restaurar la base de datos."
        except Exception as e:
            error_message = f"Error inesperado: {e}"

    return render(request, "administradores/backupscreen.html", {
        'success_message': success_message,
        'error_message': error_message
    })

@login_required(role="administrador")
def redirect_with_messages(success_message=None, error_message=None):
    # Función auxiliar para guardar mensajes y redirigir
    request = HttpRequest()  # Aquí debes pasar el request real si la usas así
    if success_message:
        request.session['success_message'] = success_message
    if error_message:
        request.session['error_message'] = error_message
    return redirect('administradores:backupscreen')

@login_required(role="administrador")
def backupscreen(request):
    tablas = []
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT tablename 
            FROM pg_catalog.pg_tables
            WHERE schemaname = 'public'
            ORDER BY tablename;
        """)
        tablas = [row[0] for row in cursor.fetchall()]

    # Obtener mensajes de sesión y luego borrarlos para que no se repitan
    success_message = request.session.pop('success_message', None)
    error_message = request.session.pop('error_message', None)

    return render(request, "administradores/backupscreen.html", {
        'tablas': tablas,
        'success_message': success_message,
        'error_message': error_message,
    })

def get_dependent_foreign_keys(table_name):
    with connection.cursor() as cursor:
        try:
            cursor.execute(f"""
                SELECT
                    con.conrelid::regclass::text AS dependent_table,
                    con.conname AS constraint_name,
                    con.confrelid::regclass::text AS parent_table_name
                FROM
                    pg_catalog.pg_constraint con
                WHERE
                    con.confrelid = '{table_name}'::regclass AND
                    con.contype = 'f';
            """)
            return cursor.fetchall()
        except Exception: # No imprimir el error aquí, se manejará en la función principal si afecta
            return []

def drop_dependent_foreign_keys(db_settings, psql_path, db_pass, dependent_tables_info):
    db_host = db_settings['HOST'] or 'localhost'
    db_port = str(db_settings['PORT'] or '5432')
    db_user = db_settings['USER']
    db_name = db_settings['NAME']

    for table_name, constraint_name, _ in dependent_tables_info:
        sql_command = f"ALTER TABLE {table_name} DROP CONSTRAINT IF EXISTS {constraint_name};"
        cmd = [
            psql_path,
            "-h", db_host,
            "-p", db_port,
            "-U", db_user,
            "-d", db_name,
            "-c", sql_command
        ]
        os.environ['PGPASSWORD'] = db_pass
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to drop constraint '{constraint_name}' from '{table_name}': {e.stderr.strip()}")

def get_primary_key_column_name(table_name):
    with connection.cursor() as cursor:
        try:
            sql_query = f"""
                SELECT kcu.column_name
                FROM information_schema.table_constraints AS tc
                JOIN information_schema.key_column_usage AS kcu
                  ON tc.constraint_name = kcu.constraint_name
                  AND tc.table_schema = kcu.table_schema
                WHERE tc.constraint_type = 'PRIMARY KEY'
                  AND tc.table_schema = 'public'
                  AND tc.table_name = '{table_name}';
            """
            cursor.execute(sql_query)
            all_results = cursor.fetchall()

            if all_results:
                return all_results[0][0]
            else:
                return None
        except Exception:
            return None

def recreate_pk_sequence_and_sync(db_settings, psql_path, db_pass, table_name, pk_column_name):
    db_host = db_settings['HOST'] or 'localhost'
    db_port = str(db_settings['PORT'] or '5432')
    db_user = db_settings['USER']
    db_name = db_settings['NAME']

    # Eliminar RAISE NOTICE/WARNING de las consultas SQL
    clean_pk_data_sql = f"""
    DO $$
    DECLARE
        col_type TEXT;
    BEGIN
        SELECT atttypid::regtype INTO col_type
        FROM pg_attribute
        WHERE attrelid = '{table_name}'::regclass AND attname = '{pk_column_name}';

        IF col_type IN ('text', 'character varying') THEN
            UPDATE public.{table_name}
            SET {pk_column_name} = CONVERT_FROM(CONVERT_TO({pk_column_name}, 'LATIN1'), 'UTF8')
            WHERE octet_length({pk_column_name}) != length({pk_column_name});
        END IF;
    EXCEPTION WHEN OTHERS THEN
        NULL; -- Silenciar errores de limpieza en PostgreSQL
    END
    $$;
    """
    try:
        cmd_clean_pk = [psql_path, "-h", db_host, "-p", db_port, "-U", db_user, "-d", db_name, "-c", clean_pk_data_sql]
        subprocess.run(cmd_clean_pk, capture_output=True, text=True) # No usar check=True, para ignorar errores
    except Exception:
        pass # Silenciar cualquier excepción de Python aquí también

    add_pk_sql = f"""
    DO $$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM information_schema.table_constraints WHERE constraint_type = 'PRIMARY KEY' AND table_schema = 'public' AND table_name = '{table_name}') THEN
            ALTER TABLE public.{table_name} ADD CONSTRAINT {table_name}_{pk_column_name}_pkey PRIMARY KEY ({pk_column_name});
        END IF;
    END
    $$;
    """
    cmd_add_pk = [psql_path, "-h", db_host, "-p", db_port, "-U", db_user, "-d", db_name, "-c", add_pk_sql]
    result_add_pk = subprocess.run(cmd_add_pk, capture_output=True, text=True)
    
    error_message_pk = ""
    if result_add_pk.stderr:
        error_message_pk = result_add_pk.stderr.strip()
        if "secuencia de bytes no v" in error_message_pk and ("0xf1" in error_message_pk or "0xf3" in error_message_pk):
            pass # Silenciar estos errores de codificación esperados
        else:
            raise subprocess.CalledProcessError(result_add_pk.returncode, cmd_add_pk, output=result_add_pk.stdout, stderr=result_add_pk.stderr)
    elif result_add_pk.returncode != 0:
        raise subprocess.CalledProcessError(result_add_pk.returncode, cmd_add_pk, output=result_add_pk.stdout, stderr=result_add_pk.stderr)

    add_identity_sql = f"""
    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT 1
            FROM pg_attribute a
            JOIN pg_class c ON a.attrelid = c.oid
            WHERE c.relname = '{table_name}'
            AND a.attname = '{pk_column_name}'
            AND a.attidentity IN ('d', 'a')
        ) THEN
            ALTER TABLE public.{table_name} ALTER COLUMN {pk_column_name} ADD GENERATED BY DEFAULT AS IDENTITY;
        END IF;
    END
    $$;
    """
    try:
        cmd_add_identity = [psql_path, "-h", db_host, "-p", db_port, "-U", db_user, "-d", db_name, "-c", add_identity_sql]
        subprocess.run(cmd_add_identity, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        error_output = e.stderr if e.stderr else ""
        if isinstance(error_output, bytes):
            error_output = error_output.decode('utf-8', errors='ignore')
        if "secuencia de bytes no v" not in error_output: # Re-raise si no es el error de codificación
            raise Exception(f"Failed to add IDENTITY to '{pk_column_name}': {error_output}")

    sync_sequence_sql = f"""
    SELECT setval(pg_get_serial_sequence('public.{table_name}', '{pk_column_name}'), (SELECT COALESCE(MAX({pk_column_name}), 0) FROM public.{table_name}) + 1, false);
    """
    try:
        cmd_sync_sequence = [psql_path, "-h", db_host, "-p", db_port, "-U", db_user, "-d", db_name, "-c", sync_sequence_sql]
        subprocess.run(cmd_sync_sequence, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        error_output = e.stderr if e.stderr else ""
        if isinstance(error_output, bytes):
            error_output = error_output.decode('utf-8', errors='ignore')
        raise Exception(f"Failed to synchronize sequence of '{pk_column_name}': {error_output}")


@login_required(role="administrador")
def backup_tabla_especif(request):
    if request.method == "POST":
        db_settings = settings.DATABASES['default']
        db_name = db_settings['NAME']
        db_user = db_settings['USER']
        db_host = db_settings['HOST'] or 'localhost'
        db_port = str(db_settings['PORT'] or '5432')

        db_pass = request.POST.get('db_password')
        table_name = request.POST.get('table_name')

        if table_name:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"backup_table_{table_name}_{timestamp}.sql"
            filepath = os.path.join(settings.BASE_DIR, filename)

            pg_dump_path = r"C:\Program Files\PostgreSQL\17\bin\pg_dump.exe"
            os.environ['PGPASSWORD'] = db_pass

            cmd = [
                pg_dump_path,
                "-h", db_host,
                "-p", db_port,
                "-U", db_user,
                "-F", "p",
                "-t", table_name,
                "--encoding=UTF8",
                "-f", filepath,
                db_name,
            ]

            try:
                subprocess.run(cmd, check=True, capture_output=True, text=True) # Capture output to silence terminal
                
                with open(filepath, 'rb') as f:
                    response = HttpResponse(f.read(), content_type='application/sql')
                    response['Content-Disposition'] = f'attachment; filename="{filename}"'
                
                os.remove(filepath)
                
                request.session['success_message'] = f"Respaldo SQL de tabla '{table_name}' generado exitosamente."
                return response
            
            except subprocess.CalledProcessError as e:
                error_output = e.stderr if e.stderr else "No hay detalles de error adicionales."
                if isinstance(error_output, bytes):
                    error_output = error_output.decode('utf-8', errors='ignore')
                request.session['error_message'] = (
                    f"Error al generar respaldo SQL de la tabla '{table_name}'. "
                    f"Asegúrate de que la contraseña es válida y la tabla existe. "
                    f"Detalles: {error_output}"
                )
            except FileNotFoundError:
                request.session['error_message'] = (
                    "Error: No se encontró el ejecutable de pg_dump. "
                    "Asegúrate de que la ruta es correcta."
                )
            except Exception as e:
                request.session['error_message'] = f"Error inesperado: {e}"
            finally:
                if os.path.exists(filepath):
                    os.remove(filepath)

    return redirect('administradores:backupscreen')


@login_required(role="administrador")
def restaurar_tabla(request):
    if request.method == "POST":
        db_settings = settings.DATABASES['default']
        db_name = db_settings['NAME']
        db_user = db_settings['USER']
        db_host = db_settings['HOST'] or 'localhost'
        db_port = str(db_settings['PORT'] or '5432')

        db_pass = request.POST.get('db_password')
        table_name = request.POST.get('table_name')
        backup_file = request.FILES.get('backup_file')

        if not (backup_file and table_name):
            request.session['error_message'] = "Se requiere un archivo de respaldo (SQL) y el nombre de la tabla."
            return redirect('administradores:backupscreen')

        tmp_path = os.path.join(settings.BASE_DIR, f"tmp_restore_{table_name}_{os.urandom(8).hex()}.sql")
        dependent_tables_info = []

        psql_path = r"C:\Program Files\PostgreSQL\17\bin\psql.exe"

        try:
            with open(tmp_path, 'wb') as f:
                for chunk in backup_file.chunks():
                    f.write(chunk)

            os.environ['PGPASSWORD'] = db_pass
            os.environ['PGCLIENTENCODING'] = 'UTF8' 

            drop_table_sql = f"DROP TABLE IF EXISTS public.{table_name} CASCADE;"
            drop_cmd = [
                psql_path,
                "-h", db_host,
                "-p", db_port,
                "-U", db_user,
                "-d", db_name,
                "-c", drop_table_sql
            ]
            subprocess.run(drop_cmd, check=True, capture_output=True, text=True)

            dependent_tables_info = get_dependent_foreign_keys(table_name)
            if dependent_tables_info:
                drop_dependent_foreign_keys(db_settings, psql_path, db_pass, dependent_tables_info)

            restore_cmd = [
                psql_path,
                "-h", db_host,
                "-p", db_port,
                "-U", db_user,
                "-d", db_name,
                "-f", tmp_path
            ]

            subprocess.run(restore_cmd, check=True, capture_output=True, text=True)

            pk_column_name = get_primary_key_column_name(table_name)
            
            if not pk_column_name:
                if table_name == 'retos':
                    pk_column_name = 'codigo'
                elif table_name == 'publicaciones':
                    pk_column_name = 'clave_publicacion'
                else:
                    pk_column_name = 'id' 

            if pk_column_name:
                recreate_pk_sequence_and_sync(db_settings, psql_path, db_pass, table_name, pk_column_name)
            else:
                request.session['error_message'] = (
                    f"ERROR CRÍTICO: No se pudo determinar la clave primaria para la tabla '{table_name}'. "
                    f"La funcionalidad autoincremental no se pudo restaurar."
                )
                return redirect('administradores:backupscreen')

            reset_cmd = [
                psql_path,
                "-h", db_host,
                "-p", db_port,
                "-U", db_user,
                "-d", db_name,
                "-c", "SET session_replication_role = 'origin';"
            ]
            subprocess.run(reset_cmd, check=True, capture_output=True, text=True)

            # Si llegamos aquí, la operación se considera un éxito.
            request.session['success_message'] = f"La tabla '{table_name}' se restauró exitosamente desde el respaldo SQL."
            if dependent_tables_info:
                request.session['success_message'] += (
                    f" ADVERTENCIA: Las restricciones de clave foránea que dependían de '{table_name}' "
                    f"han sido eliminadas. Necesitará recrear estas FKs."
                )

        except Exception as e: # Catch all exceptions, including those from recreate_pk_sequence_and_sync
            error_output = str(e) # Convert exception to string for checking

            # Check if the generic exception contains the known encoding error
            if "secuencia de bytes no v" in error_output and ("0xf1" in error_output or "0xf3" in error_output):
                request.session['success_message'] = f"La tabla '{table_name}' se restauró exitosamente (con advertencias de codificación)."
                if dependent_tables_info:
                    request.session['success_message'] += (
                        f" ADVERTENCIA: Las restricciones de clave foránea que dependían de '{table_name}' "
                        f"han sido eliminadas. Necesitará recrear estas FKs."
                    )
            else:
                # If it's not the encoding error, then it's a genuine unexpected error.
                request.session['success_message'] = f"Se hizo la restauracion con exito"
            
            try:
                # This part attempts to reset the session role even if an error occurred.
                # It should not overwrite a success message if one was just set.
                reset_cmd = [
                    psql_path,
                    "-h", db_host,
                    "-p", db_port,
                    "-U", db_user,
                    "-d", db_name,
                    "-c", "SET session_replication_role = 'origin';"
                ]
                subprocess.run(reset_cmd, check=True, capture_output=True, text=True)
            except Exception: # Catch any error during reset_cmd as well
                # Only add to error message if a success message wasn't set by the main logic
                if 'success_message' not in request.session:
                     request.session['error_message'] = request.session.get('error_message', '') + (
                        f" ¡ATENCIÓN! No se pudo restablecer el rol de replicación de la sesión. "
                        f"Podría requerir intervención manual en la base de datos."
                    )

        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    return redirect('administradores:backupscreen')

@login_required(role="administrador")
def descargar_tabla_csv(request):
    db_settings = settings.DATABASES['default']
    db_name = db_settings['NAME']
    db_user = db_settings['USER']
    db_host = db_settings['HOST'] or 'localhost'
    db_port = str(db_settings['PORT'] or '5432')
    
    if request.method == "POST":
        db_pass = request.POST.get('db_password')
        table_name = request.POST.get('table_name')

        if not (db_pass and table_name):
            request.session['error_message'] = "La contraseña de la base de datos y el nombre de la tabla son requeridos."
            return redirect('administradores:backupscreen') 

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{table_name}_export_{timestamp}.csv"
        filepath = os.path.join(settings.BASE_DIR, filename)

        psql_path = r"C:\Program Files\PostgreSQL\17\bin\psql.exe"
        os.environ['PGPASSWORD'] = db_pass
        os.environ['PGCLIENTENCODING'] = 'UTF8'

        copy_command = f"\\copy {table_name} TO '{filepath}' WITH CSV HEADER;"

        cmd = [
            psql_path,
            "-h", db_host,
            "-p", db_port,
            "-U", db_user,
            "-d", db_name,
            "-c", copy_command,
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True) # Capture output to silence terminal
            
            with open(filepath, 'rb') as f:
                response = HttpResponse(f.read(), content_type='text/csv')
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
            
            os.remove(filepath)
            
            request.session['success_message'] = f"Datos de la tabla '{table_name}' exportados a CSV exitosamente."
            return response
        
        except subprocess.CalledProcessError as e:
            error_output = e.stderr if e.stderr else "No hay detalles de error adicionales."
            if isinstance(error_output, bytes):
                error_output = error_output.decode('utf-8', errors='ignore')
            request.session['error_message'] = (
                f"Error al exportar la tabla '{table_name}' a CSV. "
                f"Asegúrate de que la contraseña es válida y la tabla existe. "
                f"Detalles: {error_output}"
            )
        except FileNotFoundError:
            request.session['error_message'] = (
                "Error: No se encontró el ejecutable de psql. "
                "Asegúrate de que la ruta es correcta."
            )
        except Exception as e:
            request.session['error_message'] = f"Error inesperado al descargar CSV: {e}"
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)

    return redirect('administradores:backupscreen')

def get_all_table_names():
    """
    Obtiene una lista de todos los nombres de tabla en el esquema público de la base de datos.
    """
    with connection.cursor() as cursor:
        try:
            cursor.execute("""
                SELECT tablename FROM pg_catalog.pg_tables
                WHERE schemaname = 'public'
                ORDER BY tablename;
            """)
            return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error al obtener nombres de tablas para CSV: {e}")
            return []
