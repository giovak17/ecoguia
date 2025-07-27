from django.urls import path
from . import views

app_name = "administradores"
urlpatterns = [
    path("", views.index, name="index"),
    path("recicladoras/aprobar/", views.aprobar_recicladoras, name="aprobar_recicladoras"),
    path('administradores/recicladoras/', views.ver_recicladoras, name='ver_recicladoras'),
    path('recicladoras/crear/', views.recicladora_crear, name='recicladora_crear'),
    path('recicladoras/editar/<int:pk>/', views.recicladora_editar, name='recicladora_editar'),
    path('recicladoras/eliminar/<int:pk>/', views.recicladora_eliminar, name='recicladora_eliminar'),

    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('contenido/', views.contenido_educativo_admin, name='contenido_admin'),
    path('contenido/nuevo/', views.contenido_crear, name='contenido_crear'),
    path('contenido/<int:pk>/editar/', views.contenido_editar, name='contenido_editar'),
    path('contenido/<int:pk>/borrar/', views.contenido_borrar, name='contenido_borrar'),

    path('backup', views.backup, name='backup'),
    path('restaurar-bd/', views.restaurar_toda_db, name='restaurar_bd'),
    path('restaurar-tabla-archivo/', views.backup_tabla_especif, name='restaurar_tabla_archivo'),
    path('administradores/restaurar-tabla-predefinida/', views.restaurar_tabla, name='restaurar_tabla_especifica'),

  
]


