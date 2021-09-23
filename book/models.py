from django.db import models
from django.utils.translation import gettext as _
from django.utils import timezone

from authentication.models import User


class Book(models.Model):
    title = models.CharField(_("title"), max_length=1000, null=False, db_index=True)
    authors = models.CharField(_("authors"), max_length=1000)
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(default=timezone.now())
    updated_at = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.title
