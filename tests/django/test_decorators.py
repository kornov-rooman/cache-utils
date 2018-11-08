import pytest

from cache_utils.django_cache_decorators import caches_result

pytestmark = [
    pytest.mark.django_db,

    pytest.mark.django,
    pytest.mark.decorators,
]


def test_ping():
    assert False
