from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from decouple import config

urlpatterns = [
    path(f"{config('ADMIN_URL_PATH', default='super-secret-admin/')}", include("apps.portail_admin.urls")),
    path(f"{config('ADMIN_URL_PATH', default='super-secret-admin/')}django/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("apps.filieres.urls")),
    path("resultats/", include("apps.resultats.urls")),
    path("imports/", include("apps.imports.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
