from __future__ import unicode_literals

try:
    from django.contrib.contenttypes.fields import GenericForeignKey
except ImportError:
    from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import six

if six.PY3:
    from unittest import mock
else:
    import mock

from caching.base import CachingMixin, CachingManager, cached_method


# This global call counter will be shared among all instances of an Addon.
call_counter = mock.Mock()


class User(CachingMixin, models.Model):
    name = models.CharField(max_length=30)

    objects = CachingManager()


class Addon(CachingMixin, models.Model):
    val = models.IntegerField()
    author1 = models.ForeignKey(User)
    author2 = models.ForeignKey(User, related_name='author2_set')

    objects = CachingManager()

    class Meta:
        # without this, Postgres & SQLite return objects in different orders:
        ordering = ('pk',)

    @cached_method
    def calls(self, arg=1):
        """This is a docstring for calls()"""
        call_counter()
        return arg, call_counter.call_count


class Comment(CachingMixin, models.Model):
    object_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    object = GenericForeignKey('object_type', 'object_id')

    object2_type = models.ForeignKey(ContentType, null=True, related_name='+')
    object2_id = models.PositiveIntegerField(null=True)
    object2 = GenericForeignKey('object2_type', 'object2_id')

    objects = CachingManager()
