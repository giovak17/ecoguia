from django.urls import path

from . import views
from recicladoras import views as recicladoras_views


app_name = "usuarios"
urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("info/", views.info, name="info"),
    path("perfil/", views.perfil_usuario, name="perfil_usuario"),
    path("ranking/", views.ranking_usuarios, name="ranking_usuarios"),
    path('contenido-educativo/', views.contenido_educativo, name='contenido_educativo'),
    path('Entregas/', views.lista_entregas, name='lista_entregas'),
    path('Entregas/<int:clave>/', views.confirmar_entrega, name='confirmar_entrega'),
    path("registro/", views.usuariosregistro, name="registro"),
    # path('mapa/', views.mapa_google, name='mapa_puntos'),
    path('clasificacion',views.clasificacion, name='clasificacion_materiales'),
    path('recicladoras/<int:id_punto>/', views.detalle_punto_reciclaje, name='punto_detalle'),
    path('mostrarentregas/', views.mostrarentregas, name='mostrarentregas'),
    
    path('api/recicladoras-materiales/', views.vista_json_recicladoras_con_materiales, name='api_recicladoras_materiales'),
    path('recicladoras-materiales/', views.vista_html_recicladoras_con_materiales, name='html_recicladoras_materiales'),
    path('recicladoras/<int:id_punto>/', views.detalle_punto_reciclaje, name='punto_detalle'),
    path('recicladoras/crear/', views.recicladora_crear, name='recicladora_crear'),

    path('RetosYRecompensas/', views.RetosYRecompensas, name='RetosYRecompensas'),

    path('publicaciones/', views.publicaciones, name='publicaciones'),
    path('crear_comentario/', views.crear_comentario, name='crear_comentario'),
    path('crear_publicacion/',views.crear_publicacion,name='crear_publicacion')
    

]
