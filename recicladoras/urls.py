from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = "recicladoras"
urlpatterns = [
    path("", views.index, name="index"),
    path("entregas/", views.confirmar_entregas, name="confirmar_entregas"),
    path("agregar_punto/", views.agregar_punto, name="agregar_punto"),
    path('tipomaterial/', views.tipo_material_list, name='tipomaterial_list'),
    path('tipomaterial/', views.tipo_material_list, name='tipomaterial_list'),
    path('tipomaterial/registro/', views.tipo_material_registro, name='tipomaterial_registro'),
    path('tipomaterial/<int:pk>/update/', views.tipo_material_actualizar, name='tipomaterial_actualizar'),
    path('tipomaterial/<int:pk>/delete/', views.tipo_material_delete, name='tipomaterial_delete'),
    path('clasificacion', views.clasificacion, name='clasificacion_materiales'),

    path('solicitar/', views.solicitar_recicladora, name='solicitar_recicladora'),
    path('verpuntosreciclaje/',views.verpuntosreciclaje,name='verpuntosreciclaje'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
