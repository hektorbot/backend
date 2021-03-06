# Generated by Django 2.2.1 on 2019-05-28 01:51

from django.db import migrations, models
from django.conf import settings
from django.core.files import File
from io import BytesIO
from PIL import Image


def make_thumbnails(apps, schema_editor):
    Artwork = apps.get_model("image_processor", "Artwork")
    artworks = Artwork.objects.all()
    for artwork in artworks:
        if artwork.final_image:
            image = Image.open(artwork.final_image)
            image.thumbnail(settings.THUMBNAILS_SIZE)
            thumbnail_io = BytesIO()
            image.save(thumbnail_io, format="JPEG")
            artwork.thumbnail.save(
                "{}_thumb.jpg".format(artwork.slug), File(thumbnail_io)
            )


class Migration(migrations.Migration):

    dependencies = [("image_processor", "0004_availableverse")]

    operations = [
        migrations.AddField(
            model_name="artwork",
            name="thumbnail",
            field=models.ImageField(
                blank=True, default=None, null=True, upload_to="finals/%Y/%m/%d/"
            ),
        ),
        migrations.RunPython(make_thumbnails)
    ]
