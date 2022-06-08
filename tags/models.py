from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Tag(models.Model):
    label = models.CharField(max_length=255)

class TagItem(models.Model):
    tag = models.ForeignKey(to=Tag, on_delete=models.CASCADE)

    content_type = models.ForeignKey(to=ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()