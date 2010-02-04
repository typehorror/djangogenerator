from django.conf.urls.defaults import *
from django.conf import settings
import os

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    {% for application in project.applications.all %}(r'^{{ application.name }}/', include('{{ application.name  }}.urls')),
    {% endfor %}

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    {% if project.has_registration %}
    (r'^registration/', include('django.contrib.auth.urls')),
    url(r'^registration/logout', 'django.contrib.auth.views.logout_then_login', name='logout_then_login'),
    {% endif %}

)

urlpatterns += patterns('django.views.generic.simple',
    url(r'^$', 'direct_to_template', {'template': 'homepage.html'}, name="homepage"),
)

if settings.DEBUG:
    urlpatterns+= patterns('',
        (r'media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

