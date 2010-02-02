from django.conf.urls.defaults import *

urlpatterns = patterns('field.views',
    url(r'add/(?P<field_type>\w+)/(?P<model_id>\d+)/$', 'new_model_field_form', name='new_model_field_form'),
    url(r'view/(?P<field_type>\w+)/(?P<model_field_id>\d+)/$', 'model_field_form', name='model_field_form'),
    url(r'del/(?P<model_field_id>\d+)/$', 'model_field_del', name='model_field_del'),
    )
 
