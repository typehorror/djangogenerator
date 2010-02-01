from django import forms
from model.utils import slugify

from models import Model

class ModelForm(forms.ModelForm):
    class Meta:
        model = Model
        fields = ('name',
                  'description',
                  'verbose_name',
                  'verbose_name_plural',
                  'db_table',)

    def clean_name(self):
        name = self.cleaned_data["name"]
        name = ''.join([ '%s%s' % (x[0].upper(),x[1:]) for x in name.split(' ') if x ])
        name = slugify(name)
        return name

class NewModelForm(forms.ModelForm):
    class Meta:
        model = Model
        fields = ('name',)

    def clean_name(self):
        name = self.cleaned_data["name"]
        name = ''.join([ '%s%s' % (x[0].upper(),x[1:]) for x in name.split(' ') if x ])
        name = slugify(name)
        return name

