from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django_q.tasks import async_task
from . import service
from .forms import UploadFileForm


def index(request):
    template = loader.get_template("image_processor/index.html")
    context = {}
    return HttpResponse(template.render(context, request))


@csrf_exempt
def style_transfer(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            artwork = form.save()
            # service.make_artwork(artwork)
            async_task("image_processor.service.make_artwork", artwork)
            return HttpResponse("Style transfer started")
    else:
        form = UploadFileForm()
    return render(request, "image_processor/style-transfer.html", {"form": form})


def results_list(request):
    page = request.GET.get("page")
    artworks = service.get_artworks(page=page)
    return render(request, "image_processor/list.html", {"artworks": artworks})
