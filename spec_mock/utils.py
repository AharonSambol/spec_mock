from typing import Type, List, Callable, Dict, Any

from spec_mock.implementation import T, _spec_mock_inner

cache = {}


def _cached_spec_mock_inner(
        instance_type: Type,
        param_name: str,
        spec: Type[T],
        strict: bool,
        *,
        previous_classes: List[Type] = None
) -> T:
    if cached_result := cache.get((instance_type, param_name)):
        return cached_result
    cache[(instance_type, param_name)] = result = _spec_mock_inner(spec, strict, previous_classes=previous_classes)
    return result


def for_each_class_in_inheritance_hierarchy(cls: Type, func: Callable[[Type], Dict[str, Any]]) -> Dict[str, Any]:
    all_results = {}
    for base_cls in reversed(cls.__mro__):  # method resolution order (MRO), reversed for overriding properties
        if base_cls is object:
            continue

        all_results.update(func(base_cls))
    return all_results
