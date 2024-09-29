from ast import NodeVisitor, Attribute, Name, FunctionDef, ClassDef, Assign, parse as ast_parse
import inspect
from typing import List, Type, Dict


class InitVisitor(NodeVisitor):
    def __init__(self):
        self.self_assignments = []

    def visit_FunctionDef(self, node: FunctionDef) -> None:
        if node.name == '__init__':
            self.generic_visit(node)

    def visit_Assign(self, node: Assign) -> None:
        # Check if it's an assignment to self.something
        if isinstance(node.targets[0], Attribute) and isinstance(node.targets[0].value, Name):
            if node.targets[0].value.id == 'self':
                # Get the name of the assigned attribute
                self.self_assignments.append(node.targets[0].attr)


def find_self_assignments_in_init(cls: Type) -> List[str]:
    try:
        source_code = inspect.getsource(cls)
        ast = ast_parse(source_code)
        visitor = InitVisitor()
        visitor.visit(ast)
        return visitor.self_assignments
    except Exception:
        return []


def get_class_properties(cls: Type) -> Dict[str, None]:
    def is_dunder(name: str) -> bool:
        return name.startswith('__') and name.endswith('__')

    properties = set(find_self_assignments_in_init(cls))
    properties.update({x for x in dir(cls) if not is_dunder(x)})
    try:
        properties.update({x for x in cls.__annotations__ if not is_dunder(x)})
    except AttributeError:
        pass
    return {x: None for x in properties}
