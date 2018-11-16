from .decorators import aiocache_decorator, django_decorator

__version__ = '0.0.0'


# noinspection PyPep8Naming
class caches_result:
    django = django_decorator
    aiocache = aiocache_decorator
