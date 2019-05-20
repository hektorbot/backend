import os
import requests
import re
import uuid
from io import BytesIO
from random import randrange
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.conf import settings
from PIL import Image, ImageDraw
from .models import Artwork


def make_artwork(artwork):
    add_colored_slice(artwork)
    transfer_style(artwork)
    find_visually_similar_image(artwork)
    pixel_sort(artwork)
    make_final_image(artwork)
    return


def add_colored_slice(artwork):
    slice_color = os.getenv("COLORED_SLICE_COLOR", "#00ff00")
    slice_width = float(os.getenv("COLORED_SLICE_WIDTH", 0.05))
    image = Image.open(artwork.style_image.path)
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
    artwork.colored_image.save("colored_{}.jpg".format(artwork.id), File(image_io))
    return


def find_visually_similar_image(artwork):
    from io import FileIO
    from google.cloud import vision
    from google.cloud.vision import types
    from mimetypes import guess_type, guess_extension
    from urllib import request

    client = vision.ImageAnnotatorClient()
    content = FileIO(artwork.style_transferred_image.path).read()
    image = types.Image(content=content)
    response = client.web_detection(image=image)
    mimeType = None

    for similar_image in response.web_detection.visually_similar_images:
        [mimeType, encoding] = guess_type(similar_image.url)
        if mimeType is not None:
            extension = guess_extension(type=mimeType)
            result = request.urlretrieve(similar_image.url)
            artwork.visually_similar_image.save(
                "visually_similar_{}{}".format(artwork.id, extension),
                File(open(result[0], "rb")),
            )
            return


def transfer_style(artwork):
    try:
        r = requests.post(
            "{}/neural-style".format(os.getenv("DEEPAI_API_ROOT")),
            files={
                "content": open(
                    os.path.join(settings.MEDIA_ROOT, artwork.input_image.path), "rb"
                ),
                "style": open(
                    os.path.join(settings.MEDIA_ROOT, artwork.colored_image.path), "rb"
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
        output_filename = "style_transferred_{}.{}".format(artwork.id, type)

        artwork.style_transferred_image.save(output_filename, File(img_tmp))
    except Exception as e:
        artwork.has_failed = True
        artwork.save()
    return


def pixel_sort(artwork):
    output_file = os.path.join(settings.MEDIA_ROOT, "{}.png".format(uuid.uuid4()))
    pixel_sort_path = os.getenv("PIXEL_SORT_PATH", "pixelsort/pixelsort.py")
    cmd = """
            {} {} {} \
            -a 180 \
            -i random \
            -r 20 \
            -c 30 \
            -o {}
        """.format(
        os.getenv("PYTHON_PATH"), pixel_sort_path, artwork.input_image.path, output_file
    )
    os.system(cmd)
    artwork.pixel_sorted_image.save(
        "pixel_sorted_{}.png".format(artwork.id), File(open(output_file, "rb"))
    )
    os.remove(output_file)
    return


def make_final_image(artwork):
    canvas = Image.open(artwork.input_image.path)
    draw = ImageDraw.Draw(canvas)
    # Pixel sorted slice
    if artwork.pixel_sorted_image:
        image = Image.open(artwork.pixel_sorted_image)
        image = image.resize((canvas.width, canvas.height))
        pixel_sorted_slice_height_px = round(
            float(os.getenv("PIXEL_SORTED_SLICE_HEIGHT", 0.15)) * canvas.height
        )
        pixel_sorted_slice_pos_y = randrange(
            0, canvas.height - pixel_sorted_slice_height_px
        )
        pixel_sorted_slice = image.crop(
            (
                0,
                pixel_sorted_slice_pos_y,
                canvas.width,
                pixel_sorted_slice_pos_y + pixel_sorted_slice_height_px,
            )
        )
        canvas.paste(pixel_sorted_slice, (0, pixel_sorted_slice_pos_y))
    # Style transferred slices
    if artwork.style_transferred_image:
        image = Image.open(artwork.style_transferred_image)
        image = image.resize((canvas.width, canvas.height))
        slices_count = int(os.getenv("STYLE_TRANSFERRED_SLICES_COUNT", 8))
        slices_min_width_px = round(
            float(os.getenv("STYLE_TRANSFERRED_SLICES_MIN_WIDTH", 0.1)) * canvas.width
        )
        slices_max_width_px = round(
            float(os.getenv("STYLE_TRANSFERRED_SLICES_MAX_WIDTH", 0.6)) * canvas.width
        )
        slices_min_height_px = round(
            float(os.getenv("STYLE_TRANSFERRED_SLICES_MIN_HEIGHT", 0.03))
            * canvas.height
        )
        slices_max_height_px = round(
            float(os.getenv("STYLE_TRANSFERRED_SLICES_MAX_HEIGHT", 0.06))
            * canvas.height
        )
        for i in range(slices_count):
            slice_width_px = randrange(slices_min_width_px, slices_max_width_px)
            slice_height_px = randrange(slices_min_height_px, slices_max_height_px)
            slice_pos_x = randrange(0, canvas.width - slice_width_px)
            slice_pos_y = randrange(0, canvas.height - slice_height_px)
            slice = image.crop(
                (
                    slice_pos_x,
                    slice_pos_y,
                    slice_width_px,
                    slice_pos_y + slice_height_px,
                )
            )
            canvas.paste(slice, (slice_pos_x, slice_pos_y))
    # Visually similar image slice
    if artwork.visually_similar_image:
        image = Image.open(artwork.visually_similar_image)
        image = image.resize((canvas.width, canvas.height))
        slice_min_width_px = round(
            float(os.getenv("VISUALLY_SIMILAR_SLICE_MIN_WIDTH", 0.1)) * canvas.width
        )
        slice_max_width_px = round(
            float(os.getenv("VISUALLY_SIMILAR_SLICE_MAX_WIDTH", 0.6)) * canvas.width
        )
        slice_min_height_px = round(
            float(os.getenv("VISUALLY_SIMILAR_SLICE_MIN_HEIGHT", 0.03)) * canvas.height
        )
        slice_max_height_px = round(
            float(os.getenv("VISUALLY_SIMILAR_SLICE_MAX_HEIGHT", 0.06)) * canvas.height
        )
        slice_width_px = randrange(slices_min_width_px, slices_max_width_px)
        slice_height_px = randrange(slices_min_height_px, slices_max_height_px)
        slice_pos_x = randrange(0, canvas.width - slice_width_px)
        slice_pos_y = randrange(0, canvas.height - slice_height_px)
        slice = image.crop(
            (slice_pos_x, slice_pos_y, slice_width_px, slice_pos_y + slice_height_px)
        )
        canvas.paste(slice, (slice_pos_x, slice_pos_y))
    canvas_io = BytesIO()
    canvas.save(canvas_io, format="JPEG")
    artwork.final_image.save("final_{}.jpg".format(artwork.id), File(canvas_io))


def get_artworks(page=1, per_page=20):
    from django.core.paginator import Paginator
    from django.db.models import Q

    artworks_list = Artwork.objects.filter(
        ~Q(style_transferred_image="")
        & ~Q(style_transferred_image=None)
        & Q(has_failed=False)
    ).order_by("-create_date")
    paginator = Paginator(artworks_list, per_page)
    artworks = paginator.get_page(page)
    return artworks
