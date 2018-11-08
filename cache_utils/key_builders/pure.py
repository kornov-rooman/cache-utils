__all__ = (
    'default_cache_builder',

    'build_func_cache_key',

    'build_class_method_cache_key',
    'build_class_method_cache_key_without_self',
    'build_class_method_cache_key_without_class',
)


def build_func_cache_key(func_name: str, *args, **kwargs) -> str:
    parts = list(args)

    for k in sorted(kwargs):
        parts.append(f'{k}={kwargs[k]}')

    joined_parts = ','.join(map(str, parts))

    return f'{func_name}({joined_parts})'


def build_class_method_cache_key(method_name: str, self, *args, **kwargs) -> str:
    parts = list(args)

    for k in sorted(kwargs):
        parts.append(f'{k}={kwargs[k]}')

    joined_parts = ','.join(parts)

    return f'{self.__class__.__name__}.{method_name}({joined_parts})'


def build_class_method_cache_key_without_self(method_name: str, self, *args, **kwargs) -> str:
    parts = list(args)

    for k in sorted(kwargs):
        parts.append(f'{k}={kwargs[k]}')

    joined_parts = ','.join(parts)

    return f'{self.__class__.__name__}.{method_name}({joined_parts})'


def build_class_method_cache_key_without_class(method_name: str, _, *args, **kwargs) -> str:
    parts = list(map(str, args))

    for k in sorted(kwargs):
        parts.append(f'{k}={kwargs[k]}')

    joined_parts = ','.join(parts)

    return f'{method_name}({joined_parts})'


default_cache_builder = build_func_cache_key
