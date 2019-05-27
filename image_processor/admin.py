from django.contrib import admin
from .models import Artwork, Verse, AvailableVerse


class ArtworkAdmin(admin.ModelAdmin):
    pass


class VerseAdmin(admin.ModelAdmin):
    pass


class AvailableVerseAdmin(admin.ModelAdmin):
    pass


admin.site.register(Artwork, ArtworkAdmin)
admin.site.register(Verse, VerseAdmin)
admin.site.register(AvailableVerse, AvailableVerseAdmin)
