from django import forms

from models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name',
                  'description',
                  'has_registration',
                  'has_profile')

class NewProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name',)
