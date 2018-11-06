import pytest

from cache_utils.predicates import default_predicate, is_not_none

pytestmark = [
    pytest.mark.unit,
    pytest.mark.predicates,
]


# noinspection PyMethodMayBeStatic
class DefaultPredicateTest:
    def test_default_predicate_is_bool(self):
        assert default_predicate is bool


# noinspection PyMethodMayBeStatic
class IsNotNonePredicateTest:
    def test_ok(self):
        assert is_not_none('')
        assert is_not_none([])
        assert is_not_none({})
        assert not is_not_none(None)
