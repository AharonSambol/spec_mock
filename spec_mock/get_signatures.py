import typing
from typing import Type, Dict


def get_type_hints_of_class(cls: Type) -> Dict[str, Type]:
    type_hints = typing.get_type_hints(cls.__init__)
    type_hints.update(typing.get_type_hints(cls))

    type_hints = {
        name: typing.get_origin(hint) or hint
        for name, hint in type_hints.items()
    }
    return type_hints
