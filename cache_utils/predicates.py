__all__ = (
    'default_predicate',

    'is_not_none',
)


def is_not_none(result):
    return result is not None


default_predicate = bool
