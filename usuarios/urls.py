from django.urls import path

from . import views

app_name = "usuarios"
urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path('contenido-educativo/', views.contenido_educativo, name='contenido_educativo'),
    path('Entregas/', views.lista_entregas, name='lista_entregas'),
    path('Entregas/<int:clave>/', views.confirmar_entrega, name='confirmar_entrega'),
    path("registro/", views.usuariosregistro, name="registro"),
    path('mapa/', views.mapa_puntos_google, name='mapa_puntos'),

    path('mostrarentregas/', views.mostrarentregas, name='mostrarentregas'),

]
