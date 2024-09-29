# spec_mock
Create Mocks which completely mimic the real deal!

spec_mock act just like the rea deal!
* spec_mock won't let you use the mock in ways a real instance wouldn't allow.
* When the class changes so will your mock!

For example:
```python
from spec_mock import spec_mock

class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
        
    def talk(self):
        pass

person = spec_mock(Person)
_ = person.age # Valid
_ = person.name # Valid
_ = person.talk.side_effect = lambda: print("hi") # Valid
_ = person.gender # Invalid!
```

How is this different from MagicMock?

`MagicMock(spec=)` and `create_autospec` don't mock the attributes: 
```python
person = MagicMock(spec=Person)
_ = person.age # AttributeError: Mock object has no attribute 'age'
```
 