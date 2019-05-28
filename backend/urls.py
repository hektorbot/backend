"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.db.models import Q
from rest_framework import routers, serializers, viewsets
from image_processor.models import Artwork


class ArtworkSerializer(serializers.ModelSerializer):
    full = serializers.SerializerMethodField("get_final_image")

    class Meta:
        model = Artwork
        fields = ["id", "full", "thumbnail"]
        read_only_fields = ["id", "full", "thumbnail"]

    def get_final_image(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.final_image.url)


class ArtworkViewSet(viewsets.ModelViewSet):
    queryset = Artwork.objects.filter(
        ~Q(final_image="") & ~Q(final_image=None) & Q(has_failed=False)
    ).order_by("-create_date")
    serializer_class = ArtworkSerializer


router = routers.DefaultRouter()
router.register(r"artworks", ArtworkViewSet)


urlpatterns = [
    url(r"^rest/", include(router.urls)),
    path("admin/", admin.site.urls),
    path("image_processor/", include("image_processor.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
