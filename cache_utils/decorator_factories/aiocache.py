import functools
import logging
import typing as t

from aiocache import caches

from cache_utils.key_builders.pure import default_cache_builder
from cache_utils.predicates import default_predicate

logger = logging.getLogger(__name__)


class AsyncDecoratorFactory:
    def __init__(self, *,
                 ttl: t.Optional[int] = None,
                 predicate: t.Optional[callable] = None,

                 cache_alias: str = 'default',
                 cache_key: t.Optional[str] = None,
                 cache_key_builder: t.Optional[callable] = None):
        self.ttl = ttl
        self.predicate = predicate or default_predicate

        self.cache_alias = cache_alias
        self.cache_key = cache_key
        self.cache_key_builder = cache_key_builder or default_cache_builder

    def __call__(self, func) -> callable:
        self.fn = func
        self.co_name = self.fn.__code__.co_name

        @functools.wraps(self.fn)
        def wrapped_fn(*args, **kwargs):
            return self.wrap_fn(*args, **kwargs)

        wrapped_fn.cache_info = AsyncCacheInfo(self)
        wrapped_fn.delete_cache = AsyncDeleteCache(self)

        return wrapped_fn

    async def wrap_fn(self, *args, **kwargs) -> t.Any:
        cache = caches.get(self.cache_alias)  # aiocache

        built_cache_key = self.cache_key or self.cache_key_builder(self.co_name, *args, **kwargs)
        logger.debug(f'async_caches_result::cache_key = "{built_cache_key}"')

        result = await cache.get(built_cache_key)  # aiocache
        if self.predicate(result):
            logger.debug('async_caches_result::HIT CACHE')

            await cache.increment(f'hits::{built_cache_key}')  # aiocache
            return result

        result = await self.fn(*args, **kwargs)
        logger.debug('async_caches_result::MISS CACHE')

        await cache.increment(f'misses::{built_cache_key}')  # aiocache
        await cache.set(built_cache_key, result, ttl=self.ttl)  # aiocache
        return result


class AsyncCacheInfo:
    def __init__(self, factory: 'AsyncDecoratorFactory'):
        self._fn = factory.fn
        self._co_name = factory.co_name

        self._ttl = factory.ttl

        self._cache_alias = factory.cache_alias
        self._cache_key = factory.cache_key
        self._cache_key_builder = factory.cache_key_builder

    async def __call__(self, *args, **kwargs) -> dict:
        cache = caches.get(self._cache_alias)  # aiocache

        built_cache_key = self._cache_key or self._cache_key_builder(self._co_name, *args, **kwargs)
        logger.debug(f'cache_info::cache_key = "{built_cache_key}"')

        hits = await cache.increment(f'hits::{built_cache_key}', delta=0)  # aiocache
        misses = await cache.increment(f'misses::{built_cache_key}', delta=0)  # aiocache
        delete_cache_count = await cache.increment(f'delete_cache_count::{built_cache_key}', delta=0)  # aiocache

        return {
            'hits': hits,
            'misses': misses,
            'total': hits + misses,
            'delete_cache_count': delete_cache_count,

            'ttl': self._ttl,
            'cache_alias': self._cache_alias,
            'cache_key': built_cache_key,
        }


class AsyncDeleteCache:
    def __init__(self, factory: 'AsyncDecoratorFactory'):
        self._fn = factory.fn
        self._co_name = factory.co_name

        self._cache_alias = factory.cache_alias
        self._cache_key = factory.cache_key
        self._cache_key_builder = factory.cache_key_builder

    async def __call__(self, *args, **kwargs) -> bool:
        cache = caches.get(self._cache_alias)  # aiocache

        built_cache_key = self._cache_key or self._cache_key_builder(self._co_name, *args, **kwargs)
        logger.debug(f'delete_cache::cache_key = "{built_cache_key}"')

        await cache.increment(f'delete_cache_count::{built_cache_key}')  # aiocache
        return await cache.delete(built_cache_key)  # aiocache
