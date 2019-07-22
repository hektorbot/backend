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
from rest_framework import routers, serializers, viewsets, status
from rest_framework.response import Response
from image_processor.models import Artwork
from image_processor import service


class ArtworkSerializer(serializers.ModelSerializer):
    full = serializers.SerializerMethodField("get_final_image_url")

    class Meta:
        model = Artwork
        fields = [
            "id",
            "full",
            "thumbnail",
            "slug",
            "input_image",
            "style_image",
            "colored_image",
            "style_transferred_image",
            "visually_similar_image",
            "pixel_sorted_image",
        ]
        read_only_fields = ["id", "final_image", "thumbnail", "slug"]
        lookup_field = "slug"

    def get_final_image_url(self, obj):
        return self.context["request"].build_absolute_uri(obj.final_image.url)

    def create(self, validated_data):
        instance = Artwork.objects.create(**validated_data)
        service.make_artwork(instance)
        return instance


class ArtworkViewSet(viewsets.ModelViewSet):
    queryset = Artwork.objects.filter(
        ~Q(final_image="")
        & ~Q(final_image=None)
        & Q(has_failed=False)
        & Q(is_active=True)
    ).order_by("-create_date")
    serializer_class = ArtworkSerializer
    lookup_field = "slug"

    def create(self, request):
        serializer = ArtworkSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


router = routers.DefaultRouter()
router.register(r"artworks", ArtworkViewSet)


urlpatterns = [
    url(r"^rest/", include(router.urls)),
    path("admin/", admin.site.urls),
    path("image_processor/", include("image_processor.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
