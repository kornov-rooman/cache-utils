import pytest

import asyncio

from cache_utils import caches_result

pytestmark = [
    pytest.mark.asyncio,  # https://github.com/pytest-dev/pytest-asyncio#pytestmarkasyncio

    pytest.mark.aiocache,
    pytest.mark.decorators,
]


@caches_result.aiocache
async def get_timestamp() -> float:
    import datetime
    return datetime.datetime.now().timestamp()


@pytest.mark.slow
async def test_acceptance():
    # should calculate timestamp only once
    timestamp = await get_timestamp()
    for i in range(10):
        await asyncio.sleep(.1)
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
