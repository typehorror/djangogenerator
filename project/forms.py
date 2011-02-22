from django import forms
from django.core.exceptions import ValidationError

from models import Project
from model.models import Model

class ProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if 'owner' in kwargs:
          self.owner = kwargs['owner']
          del kwargs['owner']
        elif 'instance' in kwargs:
          self.owner = kwargs['instance'].owner
        else:
          raise TypeError, 'owner is unknow'
        super(ProjectForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
          self.fields['profile'].queryset = Model.objects.filter(application__project=kwargs['instance'])


    class Meta:
        model = Project
        fields = ('name',
                  'description',
                  'profile',)

    def clean_name(self):
        name = self.cleaned_data["name"].strip()

        if not (self.instance and self.instance.name == name ):
            if Project.objects.filter(name=name, owner=self.owner):
               raise ValidationError('%s already exists' % name)
        return name

class NewProjectForm(ProjectForm):
    class Meta:
        model = Project
        fields = ('name',)
