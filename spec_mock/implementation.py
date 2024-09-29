import functools
import inspect
from typing import TypeVar, Type, List, cast
from unittest.mock import create_autospec, MagicMock, PropertyMock

from spec_mock.ast_traverser import get_class_properties
from spec_mock.get_signatures import get_type_hints_of_class
from spec_mock.utils import for_each_class_in_inheritance_hierarchy

T = TypeVar('T')


def spec_mock(spec: Type[T], strict: bool = True) -> T:
    return _spec_mock_inner(spec, strict)


def _spec_mock_inner(spec: Type[T], strict: bool, *, previous_classes: List[Type] = None) -> T:
    previous_classes = [spec, *(previous_classes if previous_classes else [])]

    mock_instance = create_autospec(spec, instance=True)

    properties = for_each_class_in_inheritance_hierarchy(spec, get_class_properties).keys()
    type_hints = for_each_class_in_inheritance_hierarchy(spec, get_type_hints_of_class)

    for param_name in properties:
        param_type = type_hints.get(param_name, None)
        if param_type in previous_classes:
            # To avoid exceeding recursion depth, evaluate this lazily
            property_mock = PropertyMock(
                side_effect=functools.partial(
                    _cached_spec_mock_inner,
                    type(mock_instance),
                    param_name,
                    param_type,
                    strict,
                    previous_classes=previous_classes
                )
            )
            setattr(type(mock_instance), param_name, property_mock)
        else:
            if inspect.isclass(param_type):
                param_mock = _spec_mock_inner(cast(Type[T], param_type), strict, previous_classes=previous_classes)
            else:
                if strict:
                    class Empty:
                        pass

                    param_mock = MagicMock(spec_set=Empty)
                else:
                    param_mock = MagicMock()
            setattr(mock_instance, param_name, param_mock)

    return mock_instance


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