import typing as t

from .decorator_factories import AsyncDecoratorFactory, DecoratorFactory


def django_decorator(
        func: t.Optional[callable] = None,
        *,
        ttl: t.Optional[int] = None,
        predicate: t.Optional[callable] = None,

        cache_alias: str = 'default',
        cache_key: t.Optional[str] = None,
        cache_key_builder: t.Optional[callable] = None
):
    factory_kwargs = {
        'ttl': ttl,
        'predicate': predicate,
        'cache_alias': cache_alias,
        'cache_key': cache_key,
        'cache_key_builder': cache_key_builder
    }

    if callable(func):
        return DecoratorFactory(**factory_kwargs)(func)
    return DecoratorFactory(**factory_kwargs)


def aiocache_decorator(
        func: t.Optional[callable] = None,
        *,
        ttl: t.Optional[int] = None,
        predicate: t.Optional[callable] = None,

        cache_alias: str = 'default',
        cache_key: t.Optional[str] = None,
        cache_key_builder: t.Optional[callable] = None
):
    factory_kwargs = {
        'ttl': ttl,
        'predicate': predicate,
        'cache_alias': cache_alias,
        'cache_key': cache_key,
        'cache_key_builder': cache_key_builder
    }

    if callable(func):
        return AsyncDecoratorFactory(**factory_kwargs)(func)
    return AsyncDecoratorFactory(**factory_kwargs)
