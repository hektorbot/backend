from django.forms import ModelForm
from .models import Image


class UploadFileForm(ModelForm):
    class Meta:
        model = Image
        fields = ["input_file", "style_file"]
