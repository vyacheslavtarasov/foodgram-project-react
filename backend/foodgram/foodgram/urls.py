from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("api.urls", namespace="api")),
    path("api/", include("djoser.urls")),  # Работа с пользователями
    path("api/auth/", include("djoser.urls.authtoken")),  # Работа с токенами
]
