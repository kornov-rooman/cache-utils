import typing as t

from django.db.models import Model

from cache_utils.utils import attrs_to_dict

__all__ = (
    'default_cache_builder',
    'build_django_model_cache_key',
)


def build_django_model_cache_key(func_name: str,
                                 *args,
                                 field_names: t.Sequence[str],
                                 **kwargs) -> str:
    cache_key = None

    args = list(args)
    instance = args[0]
    args = args[0:]

    # TODO: app_label, class_name

    if isinstance(instance, Model):
        fields_pattern = ':'.join('{0}:%({0})s'.format(f) for f in field_names)
        fields_part = fields_pattern % attrs_to_dict(instance, field_names)
        cache_key = ':'.join([instance.__class__._meta.app_label, instance.__class__.__name__, fields_part, func_name])

    elif issubclass(instance, Model):
        cache_key = ':'.join([instance._meta.app_label, instance.__name__, func_name])

    if cache_key is None:
        raise NotImplementedError('Can\'t build cache key for', instance)

    cache_key = cache_key.replace(' ', '_')
    return cache_key


default_cache_builder = build_django_model_cache_key
