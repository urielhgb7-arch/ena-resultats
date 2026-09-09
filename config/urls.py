from django.conf import settings
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = []

if getattr(settings, 'DEBUG', False):
    urlpatterns += [
        path(
            'debug/',
            TemplateView.as_view(template_name='debug/debug.html'),
            name='debug_interface'
        ),
    ]
