from django.urls import path

from . import views

app_name = "recicladoras"
urlpatterns = [
    path("", views.index, name="index"),
    path("entregas/", views.confirmar_entregas, name="confirmar_entregas"),
    path("agregar_punto/", views.agregar_punto, name="agregar_punto"),
    path("tipomaterial_list/", views.tipo_material_list, name=""),

]
