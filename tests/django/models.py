from django.db import models


class Profile(models.Model):
    first_name = models.CharField('First name', max_length=255, blank=False, null=False)
    last_name = models.CharField('Last name', max_length=255, blank=False, null=False)
