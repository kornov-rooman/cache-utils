import pytest

from cache_utils.key_builders.pure import build_func_cache_key

pytestmark = [
    pytest.mark.unit,
    pytest.mark.key_builders,
    pytest.mark.pure_key_builders,
]


# noinspection PyMethodMayBeStatic
class BuildFuncCacheKeyTest:
    def test_ok(self):
        cache_key = build_func_cache_key('some_function_name', 1, 2, 'three', say='hello')

        assert cache_key == 'some_function_name(1,2,three,say=hello)'
