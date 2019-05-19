from django.forms import ModelForm
from .models import Artwork


class UploadFileForm(ModelForm):
    class Meta:
        model = Artwork
        fields = ["input_image", "style_image"]
