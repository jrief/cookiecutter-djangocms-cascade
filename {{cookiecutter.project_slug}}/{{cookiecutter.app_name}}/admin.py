from django.contrib import admin
from filer.models import ThumbnailOption

admin.AdminSite.site_header = "{{ cookiecutter.project_name }}"

admin.site.unregister(ThumbnailOption)
