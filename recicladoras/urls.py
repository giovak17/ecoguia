from django.urls import path

from . import views

app_name = "recicladoras"
urlpatterns = [
    path("", views.index, name="index"),
    path("entregas/", views.confirmar_entregas, name="confirmar_entregas"),
    path("agregar_punto/", views.agregar_punto, name="agregar_punto"),
<<<<<<< HEAD
    path("tipomaterial_list/", views.tipo_material_list, name=""),

=======
    path('tipomaterial/', views.tipo_material_list, name='tipomaterial_list'),
    path('tipomaterial/', views.tipo_material_list, name='tipomaterial_list'),
    path('tipomaterial/registro/', views.tipo_material_registro, name='tipomaterial_registro'),
    path('tipomaterial/<int:pk>/update/', views.tipo_material_actualizar, name='tipomaterial_actualizar'),
    path('tipomaterial/<int:pk>/delete/', views.tipo_material_delete, name='tipomaterial_delete'),

    path('solicitar/', views.solicitar_recicladora, name='solicitar_recicladora'),
>>>>>>> 1e94b3394d24dae885092b94f9c4644951ffeef8
]
    
