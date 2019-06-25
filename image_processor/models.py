import os
from django.db import models
from django.conf import settings
from django.utils.dateformat import format
from django.utils import timezone
from PIL import Image


class Artwork(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=255, unique=True, null=True)
    input_image = models.ImageField(upload_to="%Y/%m/%d/")
    style_image = models.ImageField(upload_to="%Y/%m/%d/")
    colored_image = models.ImageField(
        upload_to="%Y/%m/%d/", default=None, blank=True, null=True
    )
    style_transferred_image = models.ImageField(
        upload_to="%Y/%m/%d/", default=None, blank=True, null=True
    )
    visually_similar_image = models.ImageField(
        upload_to="%Y/%m/%d/", default=None, blank=True, null=True
    )
    pixel_sorted_image = models.ImageField(
        upload_to="%Y/%m/%d/", default=None, blank=True, null=True
    )
    final_image = models.ImageField(
        upload_to="finals/%Y/%m/%d/", default=None, blank=True, null=True
    )
    thumbnail = models.ImageField(
        upload_to="finals/%Y/%m/%d/", default=None, blank=True, null=True
    )
    verse = models.CharField(max_length=255, default="", blank=True, null=True)
    has_failed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super(Artwork, self).save(*args, **kwargs)
        # Make slug
        self.slug = settings.ARTWORK_NAME.format(
            str(format(timezone.localtime(self.create_date), "H\hi")), int(self.id)
        )
        input_image_path = self.input_image.path
        style_image_path = self.style_image.path
        input_image = Image.open(input_image_path)
        style_image = Image.open(style_image_path)
        input_image.thumbnail((1200, 1200))
        style_image.thumbnail((1200, 1200))
        input_image.save(input_image_path)
        style_image.save(style_image_path)


class Verse(models.Model):
    text = models.CharField(max_length=255)


class AvailableVerse(models.Model):
    verse = models.ForeignKey("Verse", on_delete=models.DO_NOTHING)
