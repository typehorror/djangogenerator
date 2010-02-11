from django.conf.urls.defaults import *

urlpatterns = patterns('form.views',
    url(r'view/(?P<model_form_id>\d+)/$', 'model_form_view', name='model_form_view'),
    url(r'del/(?P<model_form_id>\d+)/$', 'model_form_del', name='model_form_del'),
    url(r'form/(?P<model_form_id>\d+)/$', 'model_form_form', name='model_form_form'),
    url(r'add/(?P<model_id>\d+)/$','new_model_form_form', name='new_model_form_form'),
    )

