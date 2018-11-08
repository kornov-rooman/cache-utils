import pytest

from cache_utils.async_cache_decorators import async_caches_result

pytestmark = [
    pytest.mark.decorators,

    pytest.mark.async,
    pytest.mark.async_cache_decorators,

    pytest.mark.aiocache,
]


@pytest.mark.django_db
def test_ping():
    assert False
