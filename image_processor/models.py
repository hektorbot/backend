from django.db import models
from PIL import Image as PILImage


class Image(models.Model):
    job_id = models.CharField(max_length=255, default="")
    job_name = models.CharField(max_length=255, default="")
    input_file = models.FileField(upload_to="uploads/%Y/%m/%d/")
    style_file = models.FileField(upload_to="uploads/%Y/%m/%d/")
    neural_output_file = models.FileField(
        upload_to="uploads/neural_style/%Y/%m/%d/", default=None, blank=True, null=True
    )

    def save(self):
        super(Image, self).save()
        input_filename = self.input_file.name
        style_filename = self.style_file.name
        input_image = PILImage.open(input_filename)
        style_image = PILImage.open(style_filename)
        input_image.thumbnail((1200, 1200))
        style_image.thumbnail((1200, 1200))
        input_image.save(input_filename)
        style_image.save(style_filename)
