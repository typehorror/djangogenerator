# -*- coding: utf-8 -*-

from django.contrib import admin
from models import *

{% for model in application.models.all %}{% if model.has_admin_view %}
class {{ model.name }}Admin(admin.ModelAdmin):
    """
    {{ model.name }} admin class
    """
    # search_fields = ('name', 'id')
    # list_filter = ('creation_date','modification_date') 
    # list_display = ('id', 'name')
    pass

admin.site.register({{ model.name }}, {{ model.name }}Admin)
{% endif %}{% endfor %}
