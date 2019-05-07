from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django_q.tasks import async_task
from . import service
from .forms import UploadFileForm
from .models import Image


def index(request):
    template = loader.get_template("image_processor/index.html")
    context = {}
    return HttpResponse(template.render(context, request))


def style_transfer(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            image_instance = form.save()
            async_task("image_processor.service.transfer_style", image_instance)
            return HttpResponse("Style transfer started")
    else:
        form = UploadFileForm()
    return render(request, "image_processor/style-transfer.html", {"form": form})


@csrf_exempt
def handle_result(request):
    service.handle_result(request)
    return HttpResponse("OK")


def results_list(request):
    page = request.GET.get("page")
    images = service.get_images(page=page)
    return render(request, "image_processor/list.html", {"images": images})
