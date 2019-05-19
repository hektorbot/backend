import os
from django.db import models
from django.conf import settings
from PIL import Image


class Artwork(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    input_image = models.ImageField(upload_to="%Y/%m/%d/")
    style_image = models.ImageField(upload_to="%Y/%m/%d/")
    colored_image = models.ImageField(
        upload_to="%Y/%m/%d/", default=None, blank=True, null=True
    )
    style_transfered_image = models.ImageField(
        upload_to="neural_style/%Y/%m/%d/", default=None, blank=True, null=True
    )
    visually_similar_image = models.ImageField(
        upload_to="%Y/%m/%d/", default=None, blank=True, null=True
    )
    has_failed = models.BooleanField(default=False)

    def save(self):
        super(Artwork, self).save()
        input_image_path = self.input_image.path
        style_image_path = self.style_image.path
        input_image = Image.open(input_image_path)
        style_image = Image.open(style_image_path)
        input_image.thumbnail((1200, 1200))
        style_image.thumbnail((1200, 1200))
        input_image.save(input_image_path)
        style_image.save(style_image_path)
