# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *  

urlpatterns = patterns('{{ application.name }}.views',{% for model in application.models.all %}
    {% if model.has_form_view %}url(r'form/{{ model.name.lower }}/(?P<{{ model.name.lower }}_id>\d+)/$', 'form_{{ model.name.lower }}', name='{{ application.name }}_{{ model.name.lower }}_form'),
    {% endif %}
    {% if model.has_read_only_view %}url(r'view/{{ model.name.lower }}/(?P<{{ model.name.lower }}_id>\d+)/$', 'view_{{ model.name.lower }}', name='{{ application.name }}_{{ model.name.lower }}_view'),
    {% endif %}
    {% if model.has_read_only_view or model.has_form_view %}url(r'list/{{ model.name.lower }}/$', 'list_{{ model.name.lower }}', name='{{ application.name }}_{{ model.name.lower }}_list'),
    {% endif %}
    {% endfor %})
