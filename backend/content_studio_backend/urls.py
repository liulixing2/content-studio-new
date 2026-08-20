from django.contrib import admin
from django.urls import include, path
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def health(_request):
    return Response({"ok": True, "service": "content-studio-backend"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health/", health),
    path("api/articles/", include("apps.articles.urls")),
]
