from django.contrib import admin

# Register your models here.
from core.models import ContenidoEducativo
from django.utils.html import format_html

@admin.register(ContenidoEducativo)
class ContenidoEducativoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'titulo', 'descripcion', 'id_usuario_ce', 'imagen', 'videos', 'video_local')
    search_fields = ('titulo', 'descripcion')
    list_filter = ('titulo',)

    fieldsets = (
        ('Información General', {
            'fields': ('titulo', 'descripcion', 'id_usuario_ce')
        }),
        ('Contenido Multimedia', {
            'fields': ('imagen', 'video_local', 'videos')
        }),
    )

    def imagen_preview(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" width="80" style="border-radius:8px;">', obj.imagen.url)
        return "Sin imagen"
    imagen_preview.short_description = "Imagen"

    def video_preview(self, obj):
        if obj.video_youtube:
            return format_html('<a href="{}" target="_blank">Ver en YouTube</a>', obj.video_youtube)
        elif obj.video_local:
            return "Video Local"
        return "Sin video"
    video_preview.short_description = "Video"