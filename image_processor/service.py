import os
import requests
import re
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.conf import settings
from .models import Artwork


def make_artwork(artwork):
    transfer_style(artwork)
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
                    os.path.join(settings.MEDIA_ROOT, artwork.style_file.path), "rb"
                ),
            },
            headers={"api-key": "e75c86af-0c17-4270-8a0f-51ea98a272ee"},
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
