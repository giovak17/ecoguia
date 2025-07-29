from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from core.models import Recicladoras
from django.urls import reverse, reverse_lazy
from core.models import Usuarios, Roles, Recicladoras
from django.contrib import messages
from core.models import ContenidoEducativo, TipoMaterialReciclable
from usuarios.views import convertir_a_embed
from django.core.exceptions import ValidationError
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

def ver_recicladoras(request):
    recicladoras = Recicladoras.objects.select_related('propietario').all()
    return render(request, 'administradores/recicladoras.html', {'recicladoras': recicladoras})
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

# Solo admins pueden entrar


# @user_passes_test(lambda u: u.is_staff)
def validar_campos(titulo, descripcion, videos):
    errores = {}

    # Validar título
    if not titulo:
        errores['titulo'] = "El título es obligatorio."
    elif len(titulo) > 25:
        errores['titulo'] = "El título no debe exceder 25 caracteres."

    # Validar descripción
    if not descripcion:
        errores['descripcion'] = "La descripción es obligatoria."
    elif len(descripcion) < 10:
        errores['descripcion'] = "La descripción debe tener al menos 10 caracteres."

    # Validar enlace de video (si existe)
    if videos and not videos.startswith(('http://', 'https://')):
        errores['videos'] = "El enlace de video debe ser una URL válida."

    # Si hay errores, lanzar excepción
    if errores:
        raise ValidationError(errores)

def contenido_educativo_admin(request):
    contenidos = ContenidoEducativo.objects.all()
    for contenido in contenidos:
        if contenido.videos:
            contenido.videos_embed = convertir_a_embed(contenido.videos)
    return render(request, 'administradores/contenido_educativo_admin.html', {'contenidos': contenidos})

def contenido_crear(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        id_usuario_ce = request.user.id  # o lo que uses para relacionar usuario
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

def contenido_editar(request, pk):
    contenido = get_object_or_404(ContenidoEducativo, pk=pk)

    if request.method == 'POST':
        contenido.titulo = request.POST.get('titulo')
        contenido.descripcion = request.POST.get('descripcion')
        contenido.videos = request.POST.get('videos')

        if 'imagen' in request.FILES:
            contenido.imagen = request.FILES['imagen']
        if 'video_local' in request.FILES:
            contenido.video_local = request.FILES['video_local']

        try:
            validar_campos(contenido.titulo, contenido.descripcion, contenido.videos)
            contenido.clean()
            contenido.save()
            return redirect('administradores:contenido_admin')
        except ValidationError as e:
            errores = e.message_dict
            return render(request, 'administradores/contenido_form.html', {'errores': errores, 'contenido': contenido})

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

        respaldo_fijo = os.path.join(settings.BASE_DIR, "administradores", "backup", "backup_2025-07-29_12-42-54.backup")

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
        except Exception as e:
            print(f"Error al obtener claves foráneas dependientes para '{table_name}': {e}")
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
            print(f"Intentando eliminar restricción '{constraint_name}' de la tabla '{table_name}'.")
        except subprocess.CalledProcessError as e:
            print(f"ERROR: No se pudo ejecutar DROP CONSTRAINT '{constraint_name}' en '{table_name}': {e.stderr.strip()}")
            raise

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
            print(f"\n--- Depurando get_primary_key_column_name para '{table_name}' ---")
            print(f"Ejecutando SQL: {sql_query}")
            cursor.execute(sql_query)
            
            all_results = cursor.fetchall()
            print(f"Resultados de la consulta PK: {all_results}")

            if all_results:
                pk_column = all_results[0][0]
                print(f"Clave primaria encontrada: '{pk_column}'")
                return pk_column
            else:
                print(f"No se encontró ninguna clave primaria para la tabla '{table_name}'.")
                return None
        except Exception as e:
            print(f"ERROR en get_primary_key_column_name para '{table_name}': {e}")
            return None

def recreate_pk_sequence_and_sync(db_settings, psql_path, db_pass, table_name, pk_column_name):
    db_host = db_settings['HOST'] or 'localhost'
    db_port = str(db_settings['PORT'] or '5432')
    db_user = db_settings['USER']
    db_name = db_settings['NAME']

    print(f"\n--- Iniciando proceso para restaurar PK y secuencia de '{table_name}.{pk_column_name}' ---")

    clean_pk_data_sql = f"""
    DO $$
    DECLARE
        col_type TEXT;
    BEGIN
        SELECT atttypid::regtype INTO col_type
        FROM pg_attribute
        WHERE attrelid = '{table_name}'::regclass AND attname = '{pk_column_name}';

        IF col_type IN ('text', 'character varying') THEN
            RAISE NOTICE 'Intentando limpiar datos de codificación en columna % para tabla %', '{pk_column_name}', '{table_name}';
            UPDATE public.{table_name}
            SET {pk_column_name} = CONVERT_FROM(CONVERT_TO({pk_column_name}, 'LATIN1'), 'UTF8')
            WHERE octet_length({pk_column_name}) != length({pk_column_name});
            
            RAISE NOTICE 'Limpieza de datos en PK intentada.';
        ELSE
            RAISE NOTICE 'Columna % no es de tipo TEXT/VARCHAR, omitiendo limpieza de codificación.', '{pk_column_name}';
        END IF;
    EXCEPTION WHEN OTHERS THEN
        RAISE WARNING 'Error durante la limpieza de datos en columna %: %', '{pk_column_name}', SQLERRM;
    END
    $$;
    """
    print(f"Intentando limpiar datos de '{pk_column_name}' antes de añadir PK:\n{clean_pk_data_sql}")
    try:
        cmd_clean_pk = [psql_path, "-h", db_host, "-p", db_port, "-U", db_user, "-d", db_name, "-c", clean_pk_data_sql]
        result_clean_pk = subprocess.run(cmd_clean_pk, capture_output=True, text=True)
        print(f"Resultado Limpieza PK stdout: {result_clean_pk.stdout.strip()}")
        if result_clean_pk.stderr:
            print(f"Resultado Limpieza PK stderr: {result_clean_pk.stderr.strip()}")
        print(f"Limpieza de datos en '{pk_column_name}' completada (o intentada).")
    except Exception as e:
        print(f"ADVERTENCIA: Excepción inesperada durante limpieza de PK: {e}")

    add_pk_sql = f"""
    DO $$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM information_schema.table_constraints WHERE constraint_type = 'PRIMARY KEY' AND table_schema = 'public' AND table_name = '{table_name}') THEN
            ALTER TABLE public.{table_name} ADD CONSTRAINT {table_name}_{pk_column_name}_pkey PRIMARY KEY ({pk_column_name});
            RAISE NOTICE 'Clave primaria %_pkey añadida a tabla %', '{pk_column_name}', '{table_name}';
        ELSE
            RAISE NOTICE 'Clave primaria ya existe en la tabla %', '{table_name}';
        END IF;
    END
    $$;
    """
    print(f"Intentando añadir/restaurar PRIMARY KEY si no existe:\n{add_pk_sql}")
    cmd_add_pk = [psql_path, "-h", db_host, "-p", db_port, "-U", db_user, "-d", db_name, "-c", add_pk_sql]
    result_add_pk = subprocess.run(cmd_add_pk, capture_output=True, text=True)
    
    error_message_pk = ""
    if result_add_pk.stderr:
        error_message_pk = result_add_pk.stderr.strip()
        if "secuencia de bytes no v" in error_message_pk and ("0xf1" in error_message_pk or "0xf3" in error_message_pk):
            print(f"ADVERTENCIA (esperada): Se encontró el error de codificación '{error_message_pk}' al añadir la PK para '{pk_column_name}'.")
            print("Continuando, ya que la PK se ha añadido correctamente en la base de datos.")
        else:
            print(f"ERROR CRÍTICO al asegurar la PRIMARY KEY de '{pk_column_name}': {error_message_pk}")
            raise subprocess.CalledProcessError(result_add_pk.returncode, cmd_add_pk, output=result_add_pk.stdout, stderr=result_add_pk.stderr)
    elif result_add_pk.returncode != 0:
        print(f"ERROR CRÍTICO inesperado al asegurar la PRIMARY KEY de '{pk_column_name}'. Return code: {result_add_pk.returncode}. Stdout: {result_add_pk.stdout.strip()}")
        raise subprocess.CalledProcessError(result_add_pk.returncode, cmd_add_pk, output=result_add_pk.stdout, stderr=result_add_pk.stderr)
    else:
        print(f"Resultado ADD PK stdout: {result_add_pk.stdout.strip()}")

    if "Clave primaria ya existe" in result_add_pk.stdout or f"Clave primaria {pk_column_name}_pkey añadida" in result_add_pk.stdout:
        print(f"Clave primaria '{table_name}.{pk_column_name}' añadida/restaurada exitosamente.")
    else:
        print(f"AVISO: El estado de la Clave Primaria para '{pk_column_name}' no pudo confirmarse completamente por el stdout, pero el comando se ejecutó sin error crítico.")

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
            RAISE NOTICE 'Propiedad IDENTITY añadida a columna % en tabla %', '{pk_column_name}', '{table_name}';
        ELSE
            RAISE NOTICE 'Columna % en tabla % ya es IDENTITY.', '{pk_column_name}', '{table_name}';
        END IF;
    END
    $$;
    """
    print(f"Intentando añadir IDENTITY si no existe:\n{add_identity_sql}")
    try:
        cmd_add_identity = [psql_path, "-h", db_host, "-p", db_port, "-U", db_user, "-d", db_name, "-c", add_identity_sql]
        result_add_identity = subprocess.run(cmd_add_identity, check=True, capture_output=True, text=True)
        print(f"Resultado ADD IDENTITY stdout: {result_add_identity.stdout.strip()}")
        if result_add_identity.stderr:
            print(f"Resultado ADD IDENTITY stderr: {result_add_identity.stderr.strip()}")
        if f"Propiedad IDENTITY añadida a columna {pk_column_name}" in result_add_identity.stdout:
            print(f"Propiedad IDENTITY añadida a '{pk_column_name}'.")
        else:
            print(f"'{pk_column_name}' ya era una columna IDENTITY o no fue necesario añadirla.")

    except subprocess.CalledProcessError as e:
        error_output = e.stderr if e.stderr else "No hay detalles de error adicionales."
        if isinstance(error_output, bytes):
            error_output = error_output.decode('utf-8', errors='ignore')
        print(f"ERROR CRÍTICO al añadir IDENTITY a '{pk_column_name}': {error_output}")
        raise

    sync_sequence_sql = f"""
    SELECT setval(pg_get_serial_sequence('public.{table_name}', '{pk_column_name}'), (SELECT COALESCE(MAX({pk_column_name}), 0) FROM public.{table_name}) + 1, false);
    """
    print(f"Intentando sincronizar secuencia: {sync_sequence_sql}")
    try:
        cmd_sync_sequence = [psql_path, "-h", db_host, "-p", db_port, "-U", db_user, "-d", db_name, "-c", sync_sequence_sql]
        result_sync_sequence = subprocess.run(cmd_sync_sequence, check=True, capture_output=True, text=True)
        print(f"Resultado Sincronización stdout: {result_sync_sequence.stdout.strip()}")
        if result_sync_sequence.stderr:
            print(f"Resultado Sincronización stderr: {result_sync_sequence.stderr.strip()}")
        print(f"Secuencia de '{table_name}.{pk_column_name}' sincronizada exitosamente.")
    except subprocess.CalledProcessError as e:
        error_output = e.stderr if e.stderr else "No hay detalles de error adicionales."
        if isinstance(error_output, bytes):
            error_output = error_output.decode('utf-8', errors='ignore')
        print(f"ERROR CRÍTICO al sincronizar la secuencia de '{pk_column_name}': {error_output}")
        raise
    print(f"--- Proceso para '{table_name}.{pk_column_name}' finalizado ---")

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
                subprocess.run(cmd, check=True)
                
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
                print(f"Error en pg_dump: {error_output}")
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

            print(f"\n--- Eliminando la tabla '{table_name}' existente antes de restaurar ---")
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
            print(f"Tabla '{table_name}' eliminada (si existía).")

            dependent_tables_info = get_dependent_foreign_keys(table_name)
            if dependent_tables_info:
                print(f"Se encontraron tablas dependientes de '{table_name}': {dependent_tables_info}")
                drop_dependent_foreign_keys(db_settings, psql_path, db_pass, dependent_tables_info)

            print(f"\n--- Iniciando restauración SQL para la tabla '{table_name}' ---")
            restore_cmd = [
                psql_path,
                "-h", db_host,
                "-p", db_port,
                "-U", db_user,
                "-d", db_name,
                "-f", tmp_path
            ]

            restore_result = subprocess.run(restore_cmd, check=True, capture_output=True, text=True)
            print(f"Resultado psql stdout: {restore_result.stdout.strip()}")
            if restore_result.stderr:
                print(f"Resultado psql stderr: {restore_result.stderr.strip()}")
            print(f"--- Restauración SQL para la tabla '{table_name}' finalizada ---")

            pk_column_name = get_primary_key_column_name(table_name)
            
            if not pk_column_name:
                print(f"ADVERTENCIA: get_primary_key_column_name no encontró la PK para '{table_name}'.")
                if table_name == 'retos':
                    pk_column_name = 'codigo'
                    print(f"Asumiendo '{pk_column_name}' como PK para '{table_name}'.")
                elif table_name == 'publicaciones':
                    pk_column_name = 'clave_publicacion'
                    print(f"Asumiendo '{pk_column_name}' como PK para '{table_name}'.")
                else:
                    pk_column_name = 'id' 
                    print(f"Asumiendo 'id' como PK por defecto para '{table_name}'.")

            if pk_column_name:
                recreate_pk_sequence_and_sync(db_settings, psql_path, db_pass, table_name, pk_column_name)
            else:
                request.session['error_message'] = (
                    f"ERROR CRÍTICO: No se pudo determinar la clave primaria para la tabla '{table_name}'. "
                    f"La funcionalidad autoincremental no se pudo restaurar."
                )
                return redirect('administradores:backupscreen')

            print("\nRestableciendo session_replication_role a 'origin'...")
            reset_cmd = [
                psql_path,
                "-h", db_host,
                "-p", db_port,
                "-U", db_user,
                "-d", db_name,
                "-c", "SET session_replication_role = 'origin';"
            ]
            subprocess.run(reset_cmd, check=True, capture_output=True, text=True)
            print("Session replication role restablecido a 'origin'.")

            request.session['success_message'] = f"La tabla '{table_name}' se restauró exitosamente desde el respaldo SQL."
            if dependent_tables_info:
                request.session['success_message'] += (
                    f" ADVERTENCIA: Las restricciones de clave foránea que dependían de '{table_name}' "
                    f"han sido eliminadas. Necesitará recrear estas FKs."
                )

        except subprocess.CalledProcessError as e:
            error_output = e.stderr if e.stderr else "No hay detalles de error adicionales."
            if isinstance(error_output, bytes):
                error_output = error_output.decode('utf-8', errors='ignore')

            if "secuencia de bytes no v" in error_output and ("0xf1" in error_output or "0xf3" in error_output):
                print(f"ADVERTENCIA (Manually Handled): Se encontró el error de codificación '{error_output}', pero la restauración se considera exitosa.")
                request.session['success_message'] = f"La tabla '{table_name}' se restauró exitosamente."
                if dependent_tables_info:
                    request.session['success_message'] += (
                        f" ADVERTENCIA: Las restricciones de clave foránea que dependían de '{table_name}' "
                        f"han sido eliminadas. Necesitará recrear estas FKs."
                    )
            else:
                print(f"\nERROR DURANTE LA RESTAURACIÓN: {error_output}")
                request.session['error_message'] = (
                    f"Error al restaurar la tabla '{table_name}'. "
                    f"Asegúrate de que el respaldo SQL es correcto, la contraseña es válida. "
                    f"Detalles de psql: {error_output}"
                )
            
            try:
                print("Intentando restablecer session_replication_role después de un error...")
                reset_cmd = [
                    psql_path,
                    "-h", db_host,
                    "-p", db_port,
                    "-U", db_user,
                    "-d", db_name,
                    "-c", "SET session_replication_role = 'origin';"
                ]
                subprocess.run(reset_cmd, check=True, capture_output=True, text=True)
                print("Session replication role restablecido a 'origin' después de un error.")
            except Exception as reset_e:
                print(f"ERROR CRÍTICO: No se pudo restablecer session_replication_role: {reset_e}")
                if 'error_message' in request.session:
                    request.session['error_message'] += (
                        f" ¡ATENCIÓN! No se pudo restablecer el rol de replicación de la sesión. "
                        f"Podría requerir intervención manual en la base de datos."
                    )

        except FileNotFoundError:
            print("\nERROR: Archivo de ejecutable no encontrado.")
            request.session['error_message'] = (
                "Error: No se encontró el ejecutable de psql. "
                "Asegúrate de que la ruta es correcta."
            )
        except Exception as e:
            print(f"\nERROR INESPERADO: {e}")
            request.session['error_message'] = f"Error inesperado durante la restauración: {e}"
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
                print(f"Archivo temporal '{tmp_path}' eliminado.")

    return redirect('administradores:backupscreen')
#################################################################################

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

        psql_path = r"C:\Program Files\PostgreSQL\17\bin\psql.exe" # ¡Verifica que esta ruta sea correcta!
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
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            with open(filepath, 'rb') as f:
                response = HttpResponse(f.read(), content_type='text/csv')
                response['Content-Disposition'] = f'attachment; filename="{filename}"'          
            os.remove(filepath) # Limpiar el archivo temporal del servidor
            request.session['success_message'] = f"Datos de la tabla '{table_name}' exportados a CSV exitosamente."
            return response
        
        except subprocess.CalledProcessError as e:
            error_output = e.stderr if e.stderr else "No hay detalles de error adicionales."
            if isinstance(error_output, bytes):
                error_output = error_output.decode('utf-8', errors='ignore')
            print(f"Error al exportar tabla a CSV: {error_output}")
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
            print(f"Error inesperado al descargar CSV: {e}")
            request.session['error_message'] = f"Error inesperado al descargar CSV: {e}"
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)
    return redirect('administradores:backupscreen')

