# -*- coding: utf-8 -*-

from django import forms

from models import *

{% for model in application.models.all %}
class {{ model.name }}Form(forms.ModelForm):
    class Meta:
        model = {{ model.name }}
{% for model_form in model.model_forms.all %}
class {{ model_form.name }}(forms.ModelForm):
    class Meta:
        model = {{ model_form.model.name }}
        fields = [{% for model_field in model_form.model_fields.all %}'{{ model_field.object.name }}'{% if not forloop.last %},
                  {% endif %}{% endfor %}]
{% endfor %}
{% endfor %}

