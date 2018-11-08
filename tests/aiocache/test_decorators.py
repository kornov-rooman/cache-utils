import pytest

from cache_utils.async_cache_decorators import async_caches_result

pytestmark = [
    pytest.mark.asyncio,  # https://github.com/pytest-dev/pytest-asyncio#pytestmarkasyncio

    pytest.mark.aiocache,
    pytest.mark.decorators,
]


@async_caches_result()
async def get_timestamp() -> float:
    import datetime
    return datetime.datetime.now().timestamp()


async def test_acceptance():
    # should calculate timestamp only once
    timestamp = await get_timestamp()
    for i in range(10):
        assert await get_timestamp() == timestamp

    # should return correct cache info
    assert await get_timestamp.cache_info() == {
        'hits': 10,
        'misses': 1,
        'total': 11,
        'delete_cache_count': 0,

        'ttl': None,
        'cache_alias': 'default',
        'cache_key': 'get_timestamp()',
    }

    # should return positive value if cache was deleted successfully
    assert await get_timestamp.delete_cache()

    # should recalculate timestamp and return correct cache info
    assert await get_timestamp() != timestamp
    assert await get_timestamp.cache_info() == {
        'hits': 10,
        'misses': 2,
        'total': 12,
        'delete_cache_count': 1,

        'ttl': None,
        'cache_alias': 'default',
        'cache_key': 'get_timestamp()',
    }
