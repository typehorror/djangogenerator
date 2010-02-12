from django import forms
from django.core.exceptions import ValidationError

from model.utils import slugify

from models import Application

class ApplicationForm(forms.ModelForm):
    def __init__(self, project, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)
        self.project = project

    class Meta:
        model = Application
        fields = ('name',)

    def clean_name(self):
        name = slugify(self.cleaned_data["name"])

        if not (self.instance and self.instance.name == name ):
            if Application.objects.filter(name=name, project=self.project):
               raise ValidationError('%s is already in use in this project' % name)
        return name

class NewApplicationForm(ApplicationForm):
    class Meta:
        model = Application
        fields = ('name',)
