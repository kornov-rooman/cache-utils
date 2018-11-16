import logging
import typing as t
import functools

from django.core.cache import DEFAULT_CACHE_ALIAS, caches

from cache_utils.key_builders.django import default_cache_builder
from cache_utils.predicates import default_predicate

logger = logging.getLogger(__name__)


class DecoratorFactory:
    def __init__(self, *,
                 ttl: t.Optional[int] = None,
                 predicate: t.Optional[callable] = None,

                 cache_alias: str = 'default',
                 cache_key: t.Optional[str] = None,
                 cache_key_builder: t.Optional[callable] = None):
        self.ttl = ttl
        self.predicate = predicate or default_predicate

        self.cache_alias = cache_alias or DEFAULT_CACHE_ALIAS
        self.cache_key = cache_key
        self.cache_key_builder = cache_key_builder or default_cache_builder

    def __call__(self, func) -> callable:
        self.fn = func
        self.co_name = self.fn.__code__.co_name

        @functools.wraps(self.fn)
        def wrapped_fn(*args, **kwargs):
            return self.wrap_fn(*args, **kwargs)

        wrapped_fn.cache_info = CacheInfo(self)
        wrapped_fn.delete_cache = DeleteCache(self)

        return wrapped_fn

    def wrap_fn(self, *args, **kwargs) -> t.Any:
        cache = caches[self.cache_alias]  # django cache

        built_cache_key = self.cache_key or self.cache_key_builder(self.co_name, *args, **kwargs, field_names=['id'])
        logger.debug(f'cache_key = "{built_cache_key}"')

        result = cache.get(built_cache_key)  # django cache
        if self.predicate(result):
            logger.debug('HIT CACHE')

            if cache.get(f'hits::{built_cache_key}') is None:
                cache.set(f'hits::{built_cache_key}', 0)
            cache.incr(f'hits::{built_cache_key}')  # django cache
            return result

        result = self.fn(*args, **kwargs)
        logger.debug('MISS CACHE')

        if cache.get(f'misses::{built_cache_key}') is None:
            cache.set(f'misses::{built_cache_key}', 0)
        cache.incr(f'misses::{built_cache_key}')  # django cache
        cache.set(built_cache_key, result, self.ttl)  # django cache
        return result


class CacheInfo:
    def __init__(self, factory: 'DecoratorFactory'):
        self._fn = factory.fn
        self._co_name = factory.co_name

        self._ttl = factory.ttl

        self._cache_alias = factory.cache_alias
        self._cache_key = factory.cache_key
        self._cache_key_builder = factory.cache_key_builder

    def __call__(self, *args, **kwargs) -> dict:
        cache = caches[self._cache_alias]  # django cache

        built_cache_key = self._cache_key or self._cache_key_builder(self._co_name, *args, **kwargs, field_names=['id'])
        logger.debug(f'AsyncCacheInfo::cache_key = "{built_cache_key}"')

        if cache.get(f'hits::{built_cache_key}') is None:
            cache.set(f'hits::{built_cache_key}', 0)
        hits = cache.incr(f'hits::{built_cache_key}', 0)  # django cache
        if cache.get(f'misses::{built_cache_key}') is None:
            cache.set(f'misses::{built_cache_key}', 0)
        misses = cache.incr(f'misses::{built_cache_key}', 0)  # django cache
        if cache.get(f'delete_cache_count::{built_cache_key}') is None:
            cache.set(f'delete_cache_count::{built_cache_key}', 0)
        delete_cache_count = cache.incr(f'delete_cache_count::{built_cache_key}', 0)  # django cache

        return {
            'hits': hits,
            'misses': misses,
            'total': hits + misses,
            'delete_cache_count': delete_cache_count,

            'ttl': self._ttl,
            'cache_alias': self._cache_alias,
            'cache_key': built_cache_key,
        }


class DeleteCache:
    def __init__(self, factory: 'DecoratorFactory'):
        self._fn = factory.fn
        self._co_name = factory.co_name

        self._cache_alias = factory.cache_alias
        self._cache_key = factory.cache_key
        self._cache_key_builder = factory.cache_key_builder

    def __call__(self, *args, **kwargs) -> bool:
        cache = caches[self._cache_alias]  # django cache

        built_cache_key = self._cache_key or self._cache_key_builder(self._co_name, *args, **kwargs, field_names=['id'])
        logger.debug(f'delete_cache::cache_key = "{built_cache_key}"')

        if cache.get(f'delete_cache_count::{built_cache_key}') is None:
            cache.set(f'delete_cache_count::{built_cache_key}', 0)
        cache.incr(f'delete_cache_count::{built_cache_key}')  # django cache
        return cache.delete(built_cache_key) or True  # django cache
