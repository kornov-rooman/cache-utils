import typing as t


# noinspection PyPep8Naming
class caches_result:
    @staticmethod
    def django(
            func: t.Optional[callable] = None,
            *,
            ttl: t.Optional[int] = None,
            predicate: t.Optional[callable] = None,

            cache_alias: str = 'default',
            cache_key: t.Optional[str] = None,
            cache_key_builder: t.Optional[callable] = None
    ):
        from .decorator_factories.django import DecoratorFactory

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

    @staticmethod
    def aiocache(
            func: t.Optional[callable] = None,
            *,
            ttl: t.Optional[int] = None,
            predicate: t.Optional[callable] = None,

            cache_alias: str = 'default',
            cache_key: t.Optional[str] = None,
            cache_key_builder: t.Optional[callable] = None
    ):
        from .decorator_factories.aiocache import AsyncDecoratorFactory

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
