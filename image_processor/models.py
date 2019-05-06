import os
from django.db import models
from django.conf import settings
from PIL import Image as PILImage


class Image(models.Model):
    job_id = models.CharField(max_length=255, default="")
    job_name = models.CharField(max_length=255, default="")
    input_file = models.FileField(upload_to="%Y/%m/%d/")
    style_file = models.FileField(upload_to="%Y/%m/%d/")
    neural_output_file = models.FileField(
        upload_to="neural_style/%Y/%m/%d/", default=None, blank=True, null=True
    )
    has_failed = models.BooleanField(default=False)

    def save(self):
        super(Image, self).save()
        input_filepath = self.input_file.path
        style_filepath = self.style_file.path
        input_image = PILImage.open(input_filepath)
        style_image = PILImage.open(style_filepath)
        input_image.thumbnail((1200, 1200))
        style_image.thumbnail((1200, 1200))
        input_image.save(input_filepath)
        style_image.save(style_filepath)
