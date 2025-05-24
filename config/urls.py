from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("market/", include("market.urls", namespace="market")),
    path("", include("users.urls", namespace="users")),
]
