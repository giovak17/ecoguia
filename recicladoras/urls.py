from django.urls import path

from . import views

app_name = "recicladoras"
urlpatterns = [
    path("", views.index, name="index"),
    path("entregas/", views.confirmar_entregas, name="confirmar_entregas"),
]
