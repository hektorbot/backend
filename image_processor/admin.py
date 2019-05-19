from django.contrib import admin
from .models import Artwork


class ArtworkAdmin(admin.ModelAdmin):
    pass


admin.site.register(Artwork, ArtworkAdmin)
