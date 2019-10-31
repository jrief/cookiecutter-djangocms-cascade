from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from cms.sitemaps import CMSSitemap

sitemaps = {'cmspages': CMSSitemap}
admin.autodiscover()


def render_robots(request):
    permission = 'noindex' in settings.ROBOTS_META_TAGS and 'Disallow' or 'Allow'
    return HttpResponse('User-Agent: *\n%s: /\n' % permission, content_type='text/plain')


urlpatterns = [
    url(r'^robots\.txt$', render_robots),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]
urlpatterns.extend(i18n_patterns(
    url(r'^admin/', admin.site.urls),
    url(r'^', include('cms.urls')),
))
if settings.DEBUG:
    urlpatterns.extend(static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    ))
