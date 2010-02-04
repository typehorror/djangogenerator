from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from models import *
from forms import *

{% for model in application.models.all %}
{% if model.has_read_only_view %}
def view_{{ model.name.lower }}(request, {{ model.name.lower }}_id):
    """
    Allow input of data on {{ model.name.lower }}
    """
    {{ model.name.lower }} = get_object_or_404({{ model.name }} ,pk={{ model.name.lower }}_id)
    context = {'{{ model.name.lower }}': {{ model.name.lower }} }
    return render_to_response('view_{{ model.name.lower }}.html',
                              context,
                              context_instance=RequestContext(request))

{% endif %}
{% if model.has_read_only_view or model.has_form_view %}
def list_{{ model.name.lower }}(request):
    """
    Display a list of {{ model.name }} paginated
    """
    {{ model.name.lower }}_list = {{ model.name }}.objects.filter.all()
    paginator = Paginator({{ model.name.lower }}_list, 5)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        {{ model.name.lower }}_list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        {{ model.name.lower }}_list = paginator.page(paginator.num_pages)

    context = {'{{ model.name.lower }}_list': {{ model.name.lower }}_list }
    return render_to_response('list_{{ model.name.lower }}.html',
                              context,
                              context_instance=RequestContext(request))
{% endif %}
{% if model.has_form_view %}
def form_{{ model.name.lower }}(request, {{ model.name.lower }}_id):
    """
    Allow input of data on {{ model.name.lower }}
    """
    {{ model.name.lower }} = get_object_or_404({{ model.name }} ,pk={{ model.name.lower }}_id)
    if request.method == "POST":
        form = {{ model.name }}Form(request.POST, instance={{ model.name.lower }})
        if form.is_valid():
            form.save()
    else:
        form = {{ model.name }}Form(instance={{ model.name.lower }})

    context = {'{{ model.name.lower }}': {{ model.name.lower }},
               'form': form }

    return render_to_response('form_{{ model.name.lower }}.html',
                              context,
                              context_instance=RequestContext(request))
        
{% endif %}
{% endfor %}
