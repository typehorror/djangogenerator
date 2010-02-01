from django.conf.urls.defaults import *

urlpatterns = patterns('application.views',
    url(r'view/(?P<application_id>\d+)/$', 'application_view', name='application_view'),
    url(r'form/(?P<application_id>\d+)/$', 'application_form', name='application_form'),
    url(r'del/(?P<application_id>\d+)/$', 'application_del', name='application_del'),
    url(r'add/(?P<project_id>\d+)/$', 'new_application_form', name='new_application_form'),
    )
 
