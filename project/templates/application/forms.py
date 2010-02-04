from django import forms

from models import *

{% for model in application.models.all %}
class {{ model.name }}Form(forms.Form):
    class Meta:
        model = {{ model.name }}
{% endfor %}

