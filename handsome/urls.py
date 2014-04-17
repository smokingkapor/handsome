from django.conf import settings
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^', include('portals.urls', 'portals', 'portals')),
    url(r'^accounts/', include('accounts.urls', 'accounts', 'accounts')),

    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^{}/(?P<path>.*)$'.format(settings.MEDIA_URL.split('/')[1]),
         'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
