from django.forms import ModelForm
from .models import Image


class UploadFileForm(ModelForm):
    class Meta:
        model = Image
        fields = [
            "input_file",
            "style_file",
            "st_iterations",
            "st_style_layer_weight_exp",
            "st_content_weight_blend",
            "st_pooling",
            "st_preserve_colors",
        ]
