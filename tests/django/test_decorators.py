import pytest

from .models import Profile

pytestmark = [
    pytest.mark.django_db,

    pytest.mark.django,
    pytest.mark.decorators,
]


def test_acceptance():
    instance: 'Profile' = Profile.objects.create(first_name='Tyler', last_name='Durden')

    # should execute get_full_name only once
    assert instance.get_full_name() == 'Tyler Durden'

    # change first and last name
    instance.first_name = 'Marla'
    instance.last_name = 'Singer'
    instance.save()

    # should return old full name anyway
    for i in range(10):
        assert instance.get_full_name() == 'Tyler Durden'

    # should return correct cache info
    assert instance.get_full_name.cache_info(instance) == {
        'hits': 10,
        'misses': 1,
        'total': 11,
        'delete_cache_count': 0,

        'ttl': None,
        'cache_alias': 'default',
        'cache_key': 'django:Profile:id:1:get_full_name',
    }

    # should return positive value if cache was deleted successfully
    assert instance.get_full_name.delete_cache(instance)

    # should recalculate full name and return correct cache info
    assert instance.get_full_name() == 'Marla Singer'
    assert instance.get_full_name.cache_info(instance) == {
        'hits': 10,
        'misses': 2,
        'total': 12,
        'delete_cache_count': 1,

        'ttl': None,
        'cache_alias': 'default',
        'cache_key': 'django:Profile:id:1:get_full_name',
    }
