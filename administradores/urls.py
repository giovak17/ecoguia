from django.urls import path
from . import views

app_name = "administradores"
urlpatterns = [
    path("", views.index, name="index"),
    path('administradores/recicladoras/', views.ver_recicladoras, name='ver_recicladoras'),
]
