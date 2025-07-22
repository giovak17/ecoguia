from django.urls import path
from . import views

app_name = "administradores"
urlpatterns = [
    path("", views.index, name="index"),
    path("recicladoras/aprobar/", views.aprobar_recicladoras, name="aprobar_recicladoras"),
    path('administradores/recicladoras/', views.ver_recicladoras, name='ver_recicladoras'),
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('contenido/', views.contenido_educativo_admin, name='contenido_admin'),
    path('contenido/nuevo/', views.contenido_crear, name='contenido_crear'),
    path('contenido/<int:pk>/editar/', views.contenido_editar, name='contenido_editar'),
    path('contenido/<int:pk>/borrar/', views.contenido_borrar, name='contenido_borrar'),
  
]


