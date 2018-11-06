from .simple import (
    build_func_cache_key,
    build_class_method_cache_key,
    build_class_method_cache_key_without_self,
    build_class_method_cache_key_without_class
)

default_cache_builder = build_func_cache_key
