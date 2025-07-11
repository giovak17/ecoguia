from django.urls import path

from . import views

app_name = "recicladoras"
urlpatterns = [
    path("", views.index, name="index"),
    path("entregas/", views.confirmar_entregas, name="confirmar_entregas"),
    path("agregar_punto/", views.agregar_punto, name="agregar_punto"),
<<<<<<< HEAD
    path('tipomaterial/', views.tipo_material_list, name='tipomaterial_list'),
    path('tipomaterial/registro/', views.tipo_material_registro, name='tipomaterial_registro'),
    path('tipomaterial/<int:pk>/', views.tipo_material_detail, name='tipomaterial_detail'),
    path('tipomaterial/<int:pk>/update/', views.tipo_material_update, name='tipomaterial_update'),
    path('tipomaterial/<int:pk>/delete/', views.tipo_material_delete, name='tipomaterial_delete'),
=======
    path('solicitar/', views.solicitar_recicladora, name='solicitar_recicladora'),
>>>>>>> 27742a5 (Act BD y Mapa)
]
