from django.contrib import admin
from django.utils.html import format_html
from .models import GalleryImage

# Custom Admin Site Branding
admin.site.site_header = "MediCare Hospital Management Portal"
admin.site.site_title = "MediCare Admin"
admin.site.index_title = "Welcome to MediCare Administration"

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'caption', 'get_image_preview', 'created_at')
    search_fields = ('title', 'caption')
    readonly_fields = ('get_image_preview',)

    def get_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" height="50" style="object-fit: cover; border-radius: 4px;" />', obj.image.url)
        return "No Image"
    get_image_preview.short_description = 'Preview'


