from django.contrib import admin
from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from model.utils import slugify

class ModelField(models.Model):
    model = models.ForeignKey('model.Model', related_name="model_fields")
    content_type = models.ForeignKey(ContentType, verbose_name=_('content type'))
    object_id = models.PositiveIntegerField(_('object id'), db_index=True)
    object = generic.GenericForeignKey('content_type', 'object_id')
    
    class Meta:
        unique_together = (('model', 'content_type', 'object_id'),)
        verbose_name = _('model field')
        verbose_name_plural = _('model fields')

    def __unicode__(self):
        try:
            return self.object.__unicode__()
        except:
            return u'Warning ModelField %d is not has no object link to it' % self.pk
admin.site.register(ModelField)

class Field(models.Model):
    name = models.CharField(max_length=255)
    null = models.BooleanField(default=False)
    blank = models.BooleanField(default=False)
    default = models.CharField(max_length=255, blank=True)
    help_text = models.CharField(max_length=255, blank=True)
    primary_key = models.BooleanField(default=False)
    unique = models.BooleanField(default=False)
    verbose_name = models.CharField(max_length=255, blank=True)
    
    class Meta:
        abstract = True
    def get_options(self):
        options = []
        for field in self._meta.fields:
            if field.name not in('unicode', 'name', 'id') and self.__getattribute__(field.name):
                value = self.__getattribute__(field.name)
                if isinstance(value, (unicode, str)):
                    option = '%s="%s"' % (field.name, value)
                else:
                    option = '%s=%s' % (field.name, value)
                options.append(option)
        return options

    def __unicode__(self):
        return u"%s = models.%s(%s)" % (self.name, self.field_type, ', '.join(self.get_options()))

class RelationFieldOption(Field):
    """
    Options that belongs to relation fields
    """
    related_name = models.CharField(max_length=255, blank=True)
    relation = models.ForeignKey('model.Model')
    class Meta:
        abstract = True

class ForeignKeyField(RelationFieldOption):
    form = 'ForeignKeyFiedForm'
    field_type = 'ForeignKeyField'
admin.site.register(ForeignKeyField)

class ManyToManyField(RelationFieldOption):
    #TODO: see if "through" doesn't make the app more complex
    #through = models.ForeignKey(Model)
    form = 'ManyToManyFieldForm'
    field_type = 'ManyToManyField'
admin.site.register(ManyToManyField)


class CharField(Field):
    # indicate if this field will be returned by the the __unicode__ method
    unicode = models.BooleanField(default=False)
    choices = models.TextField(blank=True)
    max_length = models.PositiveSmallIntegerField(default=255)
    form = 'CharFieldForm'
    field_type = 'CharField'
admin.site.register(CharField)

class TextField(Field):
    form = 'TextFieldForm'
    field_type = 'TextField'
admin.site.register(TextField)


class AutoField(Field):
    form = 'AutoFieldForm'
    field_type = 'AutoField'
admin.site.register(AutoField)

class BigIntegerField(Field):
    form = 'BigIntegerFieldForm'
    field_type = 'BigIntegerField'
admin.site.register(BigIntegerField)

class BooleanField(Field):
    form = 'BooleanFieldForm'
    field_type = 'BooleanField'
admin.site.register(BooleanField)

class CommaSeparatedIntegerField(Field):
    max_length = models.PositiveSmallIntegerField(default=255)
    form = 'CommaSeparatedIntegerFieldForm'
    field_type = 'CommaSeparatedIntegerField'
admin.site.register(CommaSeparatedIntegerField)

class DateField(Field):
    auto_now = models.BooleanField(default=False)
    auto_now_add = models.BooleanField(default=False)
    form = 'DateFieldForm'
    field_type = 'DateField'
admin.site.register(DateField)

class DateTimeField(DateField):
    form = 'DateTimeFieldForm'
    field_type = 'DateTimeField'
admin.site.register(DateTimeField)

class DecimalField(Field):
    max_digits = models.PositiveSmallIntegerField(default=5)
    decimal_places = models.PositiveSmallIntegerField(default=2)
    form = 'DecimalFieldForm'
    field_type = 'DecimalField'
admin.site.register(DecimalField)

class EmailField(Field):
    max_length = models.PositiveSmallIntegerField(default=75)
    form = 'EmailFieldForm'
    field_type = 'EmailField'
admin.site.register(EmailField)

class FileField(Field):
    max_length = models.PositiveSmallIntegerField(default=100)
    upload_to = models.CharField(max_length=255)
    form = 'FileFieldForm'
    field_type = 'FileField'
admin.site.register(FileField)

class FilePathField(Field):
    path = models.CharField(max_length=255)
    match = models.CharField(max_length=255)
    recursive = models.BooleanField(default=False)
    form = 'FilePathFieldForm'
    field_type = 'FilePathField'
admin.site.register(FilePathField)

class FloatField(Field):
    form = 'FloatFieldForm'
    field_type = 'FloatField'
admin.site.register(FloatField)

class ImageField(FileField):
    height_field = models.CharField(max_length=255, blank=True)
    width_field = models.CharField(max_length=255, blank=True)
    form = 'ImageFieldForm'
    field_type = 'ImageField'
admin.site.register(ImageField)

class IntegerField(Field):
    form = 'IntegerFieldForm'
    field_type = 'IntegerField'
admin.site.register(IntegerField)

class IPAddressField(Field):
    form = 'IPAddressFieldForm'
    field_type = 'IPAddressField'
admin.site.register(IPAddressField)

class NullBooleanField(Field):
    form = 'NullBooleanFieldForm'
    field_type = 'NullBooleanField'
admin.site.register(NullBooleanField)

class PositiveIntegerField(Field):
    form = 'PositiveIntegerFieldForm'
    field_type = 'PositiveIntegerField'
admin.site.register(PositiveIntegerField)

class PositiveSmallIntegerField(Field):
    form = 'PositiveSmallIntegerFieldForm'
    field_type = 'PositiveSmallIntegerField'
admin.site.register(PositiveSmallIntegerField)

class SlugField(Field):
    max_length = models.PositiveSmallIntegerField(default=50)
    form = 'SlugFieldForm'
    field_type = 'SlugField'
admin.site.register(SlugField)

class SmallIntegerField(Field):
    form = 'SmallIntegerFieldForm'
    field_type = 'SmallIntegerField'
admin.site.register(SmallIntegerField)

class TimeField(DateField):
    form = 'TimeFieldForm'
    field_type = 'TimeField'
admin.site.register(TimeField)

class URLField(Field):
    max_length = models.PositiveSmallIntegerField(default=200)
    verify_exists = models.BooleanField(default=True)
    form = 'URLFieldForm'
    field_type = 'URLField'
admin.site.register(URLField)

class XMLField(Field):
    schema_path = models.CharField(max_length=255)
    form = 'XMLFieldForm'
    field_type = 'XMLField'
admin.site.register(XMLField)

