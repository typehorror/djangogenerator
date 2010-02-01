from django.conf.urls.defaults import *

urlpatterns = patterns('model.views',
    url(r'view/(?P<model_id>\d+)/$', 'model_view', name='model_view'),
    url(r'del/(?P<model_id>\d+)/$', 'model_del', name='model_del'),
    url(r'form/(?P<model_id>\d+)/$', 'model_form', name='model_form'),
    url(r'add/(?P<application_id>\d+)/$','new_model_form', name='new_model_form'),
    )
 
