import os
from django.db import models
from django.conf import settings
from PIL import Image as PILImage
from .validators import validate_neural_content_weight_blend


class Image(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    job_id = models.CharField(max_length=255, default="")
    job_name = models.CharField(max_length=255, default="")
    input_file = models.FileField(upload_to="%Y/%m/%d/")
    style_file = models.FileField(upload_to="%Y/%m/%d/")

    st_iterations = models.IntegerField(default=1000)
    st_style_layer_weight_exp = models.FloatField(
        default=1.0, validators=[validate_neural_content_weight_blend]
    )
    st_content_weight_blend = models.FloatField(default=1.0)
    st_pooling = models.CharField(
        max_length=3, default="avg", choices=(("avg", "avg"), ("max", "max"))
    )
    st_preserve_colors = models.BooleanField(default=False)

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
