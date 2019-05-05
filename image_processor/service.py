import os
import re
import requests
import polling
import uuid
from subprocess import check_output
from django.urls import reverse
from .models import Image


def transfer_style(image_instance):
    out = check_output(
        """
        cd {};
        floyd login -k {};
        floyd run \
            --env tensorflow-1.12 \
            --gpu2 \
            --max-runtime 900 \
            --data floydhub/datasets/imagenet-vgg-verydeep-19/3:vgg \
            --mode serve;
        """.format(
            os.getenv("FLOYD_PROJECT_DIR"), os.getenv("FLOYD_API_KEY")
        ),
        shell=True,
    )
    out = out.decode("utf-8")
    job_name = re.search("{}[0-9]+".format(os.getenv("FLOYD_PATTERN_JOB")), out)[0]
    endpoint = re.search(
        "{}[A-Za-z0-9]+".format(os.getenv("FLOYD_PATTERN_ENDPOINT")), out
    )[0]
    endpoint_health = endpoint + "/health"
    polling.poll(
        lambda: requests.get(endpoint_health).status_code == 200,
        step=3,
        poll_forever=True,
    )
    job_id = str(uuid.uuid4())
    image_instance.job_id = job_id
    image_instance.job_name = job_name
    image_instance.save()
    cb_url = (
        "https://" + os.getenv("APP_HOST") + reverse("style-transfer-result-handler")
    )
    check_output(
        """
        curl -F "input=@{}" -F "style=@{}" -F "job_id={}" -F "cb_url={}" {}
        """.format(
            image_instance.input_file,
            image_instance.style_file,
            job_id,
            cb_url,
            endpoint,
        ),
        shell=True,
    )


def handle_result(request):
    image_instance = Image.objects.get(job_id=request.POST.get("job_id"))
    image_instance.neural_output_file = request.FILES["file"]
    image_instance.save()
    job_name = image_instance.job_name
    check_output(
        """
        cd {};
        floyd login -k {};
        floyd stop {};
        floyd delete -y {};
        """.format(
            os.getenv("FLOYD_PROJECT_DIR"),
            os.getenv("FLOYD_API_KEY"),
            job_name,
            job_name,
        ),
        shell=True,
    )

