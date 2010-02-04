from django.db import models
{% for model in application.models.all %}
class {{ model.name }}(models.Model):
    {% if model.description %}"""
    {{ model.description }}
    """{% endif %}
    {% for model_field in model.model_fields.all %}
        {{ model_field.object|safe }}{% endfor %}

{% if  model.has_read_only_view or model.has_form_view %}
    @models.permalink
    def get_absolute_url(self):
        {% if  model.has_read_only_view %}return ('{{ model.application.name }}.views.view_{{ model.name.lower }}', [str(self.id)]){% else %}return ('{{ model.application.name}}.views.form_{{ model.name.lower }}', [str(self.id)]){% endif %}

{% endif %}
{% for model_field in model.model_fields.all %}{% if model_field.object.unicode %}
    def __unicode__(self):
        return self.{{ model_field.object.name }}
{% endif %}{% endfor %}{% endfor %}
