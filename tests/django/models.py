from django.db import models

from cache_utils import caches_result


class Profile(models.Model):
    first_name = models.CharField('First name', max_length=255, blank=False, null=False)
    last_name = models.CharField('Last name', max_length=255, blank=False, null=False)

    @caches_result.django
    def get_full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'
