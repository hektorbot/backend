import os
import requests
import re
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.conf import settings
from .models import Image


def transfer_style(image_instance):
    try:
        r = requests.post(
            "{}/neural-style".format(os.getenv("DEEPAI_API_ROOT")),
            files={
                "content": open(
                    os.path.join(settings.MEDIA_ROOT, image_instance.input_file.path),
                    "rb",
                ),
                "style": open(
                    os.path.join(settings.MEDIA_ROOT, image_instance.style_file.path),
                    "rb",
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

        image_instance.neural_output_file.save(output_filename, File(img_tmp))
    except Exception as e:
        image_instance.has_failed = True
        image_instance.save()
    return


def get_images(page=1, per_page=20):
    from django.core.paginator import Paginator
    from django.db.models import Q

    images_list = Image.objects.filter(
        ~Q(neural_output_file="") & ~Q(neural_output_file=None) & Q(has_failed=False)
    ).order_by("-create_date")
    paginator = Paginator(images_list, per_page)
    images = paginator.get_page(page)
    return images
