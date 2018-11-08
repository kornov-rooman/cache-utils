import pytest

from cache_utils.key_builders.django import build_django_model_cache_key

from .models import Profile

pytestmark = [
    pytest.mark.django_db,

    pytest.mark.django,
    pytest.mark.key_builders,
]


# noinspection PyMethodMayBeStatic
@pytest.mark.django_db
class BuildModelCacheKeyTest:
    def test_ok(self):
        instance = Profile.objects.create(first_name='Tyler', last_name='Durden')
        cache_key = build_django_model_cache_key(instance, ['first_name', 'last_name'], 'some_method_name')

        assert cache_key == 'django:Profile:first_name:Tyler:last_name:Durden:some_method_name'
