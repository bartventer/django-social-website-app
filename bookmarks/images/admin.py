from django.contrib import admin
from .models import Image

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    '''
    Registering the Image model in the administration site.
    '''
    list_display = ['title', 'slug', 'image', 'created']
    list_filter = ['created']
