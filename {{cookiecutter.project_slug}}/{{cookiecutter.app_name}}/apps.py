import os
from django.apps import AppConfig
from django.conf import settings


class AppConfig(AppConfig):
    name = '{{ cookiecutter.app_name }}'
    verbose_name = "{{ cookiecutter.project_name }}"

    def ready(self):
        if not os.path.isdir(settings.STATIC_ROOT):
           os.makedirs(settings.STATIC_ROOT)
        if not os.path.isdir(settings.MEDIA_ROOT):
           os.makedirs(settings.MEDIA_ROOT)
        if not os.path.isdir(settings.COMPRESS_ROOT):
           os.makedirs(settings.COMPRESS_ROOT)
