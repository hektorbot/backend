from django.forms import ModelForm
from .models import Artwork


class UploadFileForm(ModelForm):
    class Meta:
        model = Artwork
        fields = ["input_file", "style_file"]
