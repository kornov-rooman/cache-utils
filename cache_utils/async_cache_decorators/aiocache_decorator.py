import logging
import typing as t
from functools import wraps

from aiocache import caches

from cache_utils.key_builders import default_cache_builder
from cache_utils.predicates import default_predicate

logger = logging.getLogger(__name__)

__all__ = (
    'async_caches_result',
)


def async_caches_result(
        *,
        ttl: t.Optional[int] = None,
        predicate: callable = default_predicate,

        cache_alias: str = 'default',
        cache_key: t.Optional[str] = None,
        cache_key_builder: callable = default_cache_builder
):
    def _cached(func):
        co_name = func.__code__.co_name

        @wraps(func)
        async def wrapper(*args, **kwargs) -> t.Any:
            cache = caches.get(cache_alias)  # aiocache

            built_cache_key = cache_key or cache_key_builder(co_name, *args, **kwargs)
            logger.debug(f'cache_key = "{built_cache_key}"')

            result = await cache.get(built_cache_key)  # aiocache
            if predicate(result):
                logger.debug('HIT CACHE')

                await cache.increment(f'hits::{built_cache_key}')  # aiocache
                return result

            result = await func(*args, **kwargs)
            logger.debug('MISS CACHE')

            await cache.increment(f'misses::{built_cache_key}')  # aiocache
            await cache.set(built_cache_key, result, ttl=ttl)  # aiocache
            return result

        async def cache_info(*args, **kwargs) -> dict:
            cache = caches.get(cache_alias)  # aiocache

            built_cache_key = cache_key or cache_key_builder(co_name, *args, **kwargs)
            logger.debug(f'cache_info::cache_key = "{built_cache_key}"')

            hits = await cache.increment(f'hits::{built_cache_key}', delta=0)  # aiocache
            misses = await cache.increment(f'misses::{built_cache_key}', delta=0)  # aiocache
            delete_cache_count = await cache.increment(f'delete_cache_count::{built_cache_key}', delta=0)  # aiocache

            return {
                'hits': hits,
                'misses': misses,
                'total': hits + misses,
                'delete_cache_count': delete_cache_count,

                'ttl': ttl,
                'cache_alias': cache_alias,
                'cache_key': built_cache_key,
            }

        async def delete_cache(*args, **kwargs):
            cache = caches.get(cache_alias)  # aiocache

            built_cache_key = cache_key or cache_key_builder(co_name, *args, **kwargs)
            logger.debug(f'delete_cache::cache_key = "{built_cache_key}"')

            await cache.increment(f'delete_cache_count::{built_cache_key}')  # aiocache
            await cache.delete(built_cache_key)  # aiocache

        wrapper.cache_info = cache_info
        wrapper.delete_cache = delete_cache
        return wrapper

    return _cached
