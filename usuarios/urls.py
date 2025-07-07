from django.urls import path

from . import views

app_name = "usuarios"
urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path('contenido-educativo/', views.contenido_educativo, name='contenido_educativo'),
    path('Entregas/', views.lista_entregas, name='lista_entregas'),
    path('Entregas/<int:clave>/', views.confirmar_entrega, name='confirmar_entrega'),
]
