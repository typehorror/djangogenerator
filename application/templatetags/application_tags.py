from django import template
from application.forms import ApplicationForm, NewApplicationForm

register = template.Library()

@register.inclusion_tag('application_view.html')
def application_view(application):
    return {'application':application}

@register.inclusion_tag('application_form.html')
def application_form(application):
    application_form = ApplicationForm(application.project, instance=application, prefix='app_%d_' % application.id)
    return {'application': application, 'application_form': application_form}

@register.inclusion_tag('new_application_form.html')
def new_application_form(project):
	new_application_form = NewApplicationForm(project, prefix='new_application_')
	return {'new_application_form': new_application_form, 'project':project}
