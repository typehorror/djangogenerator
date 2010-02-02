from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic

from utils import slugify

class Model(models.Model):
    name = models.CharField(max_length=255)
    application = models.ForeignKey('application.Application', related_name='models')
    description = models.TextField(blank=True)

    # Meta options
    verbose_name = models.CharField(max_length=255, blank=True)
    verbose_name_plural = models.CharField(max_length=255, blank=True)
    #TODO: need to be clarified
    #app_label = models.CharField(max_length=255, blank=True)
    db_table = models.CharField(max_length=255, blank=True)

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True, auto_now_add=True)

    def __unicode__(self):
        return "%s.%s" % (self.application, self.name)

class Permissions(models.Model):
    model = models.ForeignKey(Model, related_name="permissions")
    name = models.CharField(max_length=55)
    
    def __unicode__(self):
        return '("%s", "%s")' % (slugify(self.name), self.name)

