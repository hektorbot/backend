from django.urls import path

from . import views

urlpatterns = [
    path("", views.results_list, name="results-list"),
    path("style-transfer", views.style_transfer, name="style-transfer"),
    path(
        "style-transfer/handle-result",
        views.handle_result,
        name="style-transfer-result-handler",
    ),
]
