import logging
import typing as t
from functools import wraps

from django.core.cache import DEFAULT_CACHE_ALIAS, caches

from cache_utils.key_builders.django import default_cache_builder
from cache_utils.predicates import default_predicate

logger = logging.getLogger(__name__)


def caches_result(
        *,
        ttl: t.Optional[int] = None,
        predicate: callable = default_predicate,

        cache_alias: str = DEFAULT_CACHE_ALIAS,
        cache_key: t.Optional[str] = None,
        cache_key_builder: callable = default_cache_builder,

        field_names: t.List[str] = None
):
    field_names = field_names or ['id']

    def _cached(func):
        co_name = func.__code__.co_name

        @wraps(func)
        def wrapper(*args, **kwargs) -> t.Any:
            cache = caches[cache_alias]  # django cache

            self = args[0]  # TODO: make it better
            built_cache_key = \
                cache_key or cache_key_builder(co_name, *args, **kwargs, instance=self, field_names=field_names)
            logger.debug(f'cache_key = "{built_cache_key}"')

            result = cache.get(built_cache_key)  # django cache
            if predicate(result):
                logger.debug('HIT CACHE')

                if cache.get(f'hits::{built_cache_key}') is None:
                    cache.set(f'hits::{built_cache_key}', 0)
                cache.incr(f'hits::{built_cache_key}')  # django cache
                return result

            result = func(*args, **kwargs)
            logger.debug('MISS CACHE')

            if cache.get(f'misses::{built_cache_key}') is None:
                cache.set(f'misses::{built_cache_key}', 0)
            cache.incr(f'misses::{built_cache_key}')  # django cache
            cache.set(built_cache_key, result, ttl)  # django cache
            return result

        def cache_info(*args, **kwargs) -> dict:
            cache = caches[cache_alias]  # django cache

            self = args[0]  # TODO: make it better
            built_cache_key = \
                cache_key or cache_key_builder(co_name, *args, **kwargs, instance=self, field_names=field_names)
            logger.debug(f'cache_info::cache_key = "{built_cache_key}"')

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

                'ttl': ttl,
                'cache_alias': cache_alias,
                'cache_key': built_cache_key,
            }

        def delete_cache(*args, **kwargs) -> bool:
            cache = caches[cache_alias]  # django cache

            self = args[0]  # TODO: make it better
            built_cache_key = \
                cache_key or cache_key_builder(co_name, *args, **kwargs, instance=self, field_names=field_names)
            logger.debug(f'delete_cache::cache_key = "{built_cache_key}"')

            if cache.get(f'delete_cache_count::{built_cache_key}') is None:
                cache.set(f'delete_cache_count::{built_cache_key}', 0)
            cache.incr(f'delete_cache_count::{built_cache_key}')  # django cache
            return cache.delete(built_cache_key) or True  # django cache

        wrapper.cache_info = cache_info
        wrapper.delete_cache = delete_cache
        return wrapper

    return _cached
