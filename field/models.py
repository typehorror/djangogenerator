from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _


from utils import slugify

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
        return self.object.__unicode__()

class Field(models.Model):
    name = models.CharField(max_length=255)
    max_length = models.IntegerField()
    choices = models.TextField(blank=True)
    null = models.BooleanField(default=False)
    blank = models.BooleanField(default=False)
    default = models.CharField(max_length=255, blank=True)
    help_text = models.CharField(max_length=255, blank=True)
    primary_key = models.BooleanField(default=False)
    unique = models.BooleanField(default=False)
    verbose_name = models.CharField(max_length=255)
    
    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name


class RelationFieldOption(Field):
    """
    Options that belongs to relation fields
    """
    related_name = models.CharField(max_length=255, blank=True)
    class Meta:
        abstract = True

class ForeignKeyField(RelationFieldOption):
    pass

class ManyToManyField(RelationFieldOption):
    #TODO: see if "through" doesn't make the app more complex
    #through = models.ForeignKey(Model)
    pass


class CharFieldOtion(Field):
    # indicate if this field will be returned by the the __unicode__ method
    unicode = models.BooleanField(default=False)

