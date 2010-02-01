from django.conf.urls.defaults import *

urlpatterns = patterns('field.views',
    url(r'add_field/(?P<model_id>\d+)/$', 'new_field_form', name='new_field_form'),
    )
 
