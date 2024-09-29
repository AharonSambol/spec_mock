from typing import Type, Callable, Dict, Any


def for_each_class_in_inheritance_hierarchy(cls: Type, func: Callable[[Type], Dict[str, Any]]) -> Dict[str, Any]:
    all_results = {}
    for base_cls in reversed(cls.__mro__):  # method resolution order (MRO), reversed for overriding properties
        if base_cls is object:
            continue

        all_results.update(func(base_cls))
    return all_results
