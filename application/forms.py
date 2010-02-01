from django import forms
from model.utils import slugify

from models import Application

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('name',)

    def clean_name(self):
        return slugify(self.cleaned_data["name"])
        

class NewApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('name',)

    def clean_name(self):
        return slugify(self.cleaned_data["name"])
