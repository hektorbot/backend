import os
import requests
import re
from random import randrange
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.conf import settings
from PIL import Image, ImageDraw
from .models import Artwork


def make_artwork(artwork):
    add_colored_slice(artwork)
    transfer_style(artwork)
    return


def add_colored_slice(artwork):
    from io import BytesIO
    from django.core.files import File

    slice_color = os.getenv("COLORED_SLICE_COLOR", "#00ff00")
    slice_width = float(os.getenv("COLORED_SLICE_WIDTH", 0.05))
    image = Image.open(artwork.style_file.path)
    # Determine slice width and position
    slice_width_px = image.width * slice_width
    x0 = randrange(0, round(image.width - slice_width))
    x1 = x0 + slice_width_px
    # Draw colored slice
    draw = ImageDraw.Draw(image)
    draw.rectangle([(x0, 0), (x1, image.height)], fill=slice_color)
    # Save the image
    image_io = BytesIO()
    image.save(image_io, format="JPEG")
    artwork.colored_file.save("colored.jpg", File(image_io))
    return


def transfer_style(artwork):
    try:
        r = requests.post(
            "{}/neural-style".format(os.getenv("DEEPAI_API_ROOT")),
            files={
                "content": open(
                    os.path.join(settings.MEDIA_ROOT, artwork.input_file.path), "rb"
                ),
                "style": open(
                    os.path.join(settings.MEDIA_ROOT, artwork.colored_file.path), "rb"
                ),
            },
            headers={"api-key": os.getenv("DEEPAI_API_KEY")},
        )
        json = r.json()
        r = requests.get(json["output_url"])
        type = re.match("image/([a-z]+)", r.headers["Content-Type"])[1]
        img_tmp = NamedTemporaryFile(delete=True)
        img_tmp.write(r.content)
        img_tmp.flush()
        output_filename = "{}.{}".format(json["id"], type)

        artwork.neural_output_file.save(output_filename, File(img_tmp))
    except Exception as e:
        artwork.has_failed = True
        artwork.save()
    return


def get_artworks(page=1, per_page=20):
    from django.core.paginator import Paginator
    from django.db.models import Q

    artworks_list = Artwork.objects.filter(
        ~Q(neural_output_file="") & ~Q(neural_output_file=None) & Q(has_failed=False)
    ).order_by("-create_date")
    paginator = Paginator(artworks_list, per_page)
    artworks = paginator.get_page(page)
    return artworks
