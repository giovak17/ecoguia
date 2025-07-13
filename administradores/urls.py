from django.urls import path
from . import views

app_name = "administradores"
urlpatterns = [
    path("", views.index, name="index"),
    path("recicladoras/aprobar/", views.aprobar_recicladoras, name="aprobar_recicladoras"),
    path('administradores/recicladoras/', views.ver_recicladoras, name='ver_recicladoras'),
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
]


