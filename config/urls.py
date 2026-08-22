from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from decouple import config

admin_prefix = config('ADMIN_URL_PATH', default='super-secret-admin/')

urlpatterns = [
    path(admin_prefix, include([
        path("", include("apps.portail_admin.urls")),
        path("filieres/", include("apps.filieres.admin_urls")),
        path("ue/", include("apps.resultats.admin_urls")),
        path("imports/", include("apps.imports.urls")),
        path("django/", admin.site.urls),
    ])),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("apps.filieres.urls")),
    path("resultats/", include("apps.resultats.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
