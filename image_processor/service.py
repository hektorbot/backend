import os
import re
import requests
import polling
import uuid
from subprocess import check_output
from django.urls import reverse
from django.conf import settings
from .models import Image


def transfer_style(image_instance):
    out = check_output(
        """
        cd {floyd_project_dir};
        {floyd_bin} login -k {floyd_api_key};
        {floyd_bin} run \
            --env tensorflow-1.12 \
            --gpu2 \
            --max-runtime 900 \
            --data floydhub/datasets/imagenet-vgg-verydeep-19/3:vgg \
            --mode serve;
        """.format(
            floyd_bin=os.getenv("FLOYD_BIN_PATH"),
            floyd_project_dir=os.getenv("FLOYD_PROJECT_DIR"),
            floyd_api_key=os.getenv("FLOYD_API_KEY"),
        ),
        shell=True,
    )
    out = out.decode("utf-8")
    job_name = re.search("{}[0-9]+".format(os.getenv("FLOYD_PATTERN_JOB")), out)[0]
    endpoint = re.search(
        "{}[A-Za-z0-9]+".format(os.getenv("FLOYD_PATTERN_ENDPOINT")), out
    )[0]
    endpoint_health = endpoint + "/health"
    try:
        polling.poll(
            lambda: requests.get(endpoint_health).status_code == 200,
            step=3,
            poll_forever=False,
            timeout=120,
        )
        job_id = str(uuid.uuid4())
        cb_url = (
            "https://"
            + os.getenv("APP_HOST")
            + reverse("style-transfer-result-handler")
        )
        check_output(
            """
            curl \
                -F "input=@{}" \
                -F "style=@{}" \
                -F "job_id={}" \
                -F "cb_url={}" \
                {}
            """.format(
                os.path.join(settings.MEDIA_ROOT, image_instance.input_file.path),
                os.path.join(settings.MEDIA_ROOT, image_instance.style_file.path),
                job_id,
                cb_url,
                endpoint,
            ),
            shell=True,
        )
        image_instance.job_id = job_id
        image_instance.job_name = job_name
        image_instance.save()
    except:
        image_instance.has_failed = True
        image_instance.save()
    return


def handle_result(request):
    image_instance = Image.objects.get(job_id=request.POST.get("job_id"))
    image_instance.neural_output_file = request.FILES["file"]
    image_instance.save()
    job_name = image_instance.job_name
    check_output(
        """
        cd {floyd_project_dir};
        {floyd_bin} login -k {floyd_api_key};
        {floyd_bin} stop {job_name};
        {floyd_bin} delete -y {job_name};
        """.format(
            floyd_bin=os.getenv("FLOYD_BIN_PATH"),
            floyd_project_dir=os.getenv("FLOYD_PROJECT_DIR"),
            floyd_api_key=os.getenv("FLOYD_API_KEY"),
            job_name=job_name,
        ),
        shell=True,
    )
    return


def get_images(page=1, per_page=20):
    from django.core.paginator import Paginator
    from django.db.models import Q

    images_list = Image.objects.filter(
        ~Q(neural_output_file="") & ~Q(neural_output_file=None) & Q(has_failed=False)
    )
    paginator = Paginator(images_list, per_page)
    images = paginator.get_page(page)
    return images
