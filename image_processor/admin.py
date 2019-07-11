from django.utils.safestring import mark_safe
from django.contrib import admin
from .models import Artwork, Verse, AvailableVerse


def make_inactive(modeladmin, request, queryset):
    queryset.update(is_active=False)


make_inactive.short_description = "Mark selected artworks as inactive"


def make_active(modeladmin, request, queryset):
    queryset.update(is_active=True)


make_active.short_description = "Mark selected artworks as active"


class ArtworkAdmin(admin.ModelAdmin):
    readonly_fields = ["thumbnail_image"]

    def thumbnail_image(self, obj):
        if not obj.thumbnail:
            return ""
        return mark_safe(
            '<img src="{url}" width="{width}" height={height} />'.format(
                url=obj.thumbnail.url,
                width=obj.thumbnail.width,
                height=obj.thumbnail.height,
            )
        )

    list_display = ["id", "verse", "thumbnail_image", "is_active"]
    list_display_links = ["id", "verse", "thumbnail_image"]
    actions = [make_inactive, make_active]


class VerseAdmin(admin.ModelAdmin):
    pass


class AvailableVerseAdmin(admin.ModelAdmin):
    pass


admin.site.register(Artwork, ArtworkAdmin)
admin.site.register(Verse, VerseAdmin)
admin.site.register(AvailableVerse, AvailableVerseAdmin)
