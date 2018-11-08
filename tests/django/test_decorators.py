import pytest

from cache_utils.django_cache_decorators import caches_result

pytestmark = [
    pytest.mark.decorators,

    pytest.mark.django,
    pytest.mark.django_cache_decorators,
]


@pytest.mark.django_db
def test_ping():
    assert False
