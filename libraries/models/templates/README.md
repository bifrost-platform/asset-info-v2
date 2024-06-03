# Models.Templates

This library contains templates for creating new models.

## Table of Contents

- [Models.Templates](#modelstemplates)
    - [Table of Contents](#table-of-contents)
    - [List of Templates](#list-of-templates)
        - [Camelcase Model](#camelcase-model)
        - [Enum Model](#enum-model)
        - [List Model](#list-model)
        - [String Model](#string-model)

## List of Templates

### [Camelcase Model](./camelcase_model.py)

The `CamelCaseModel` is a template for creating new camelcase object models.
It is a subclass of `BaseModel` and provides a `model_dump` method for converting the model's keys to camelcase.

```python
from libraries.models.templates.camelcase_model import CamelCaseModel


class MyModel(CamelCaseModel):
    sample_key: str


model = MyModel.model_validate({"sampleKey": "sample"})

print(model.model_dump(mode="json"))
# {"sampleKey": "sample"}
print(model.sample_key)
# sample
```

### [Enum Model](./enum_model.py)

The `EnumModel` is a template for creating new enum models.
It is a subclass of `RootModel` and provides ordering, equality, and conversion from and to string.

```python
from enum import StrEnum
from typing import Self

from libraries.models.templates.enum_model import EnumModel


class _MyEnum(StrEnum):
    A = "a"
    B = "b"
    C = "c"


class MyEnumModel(EnumModel[_MyEnum]):
    @classmethod
    def ascending_list(cls) -> list[Self]:
        return [MyEnumModel(enum) for enum in _MyEnum]


a = MyEnumModel("a")
b = MyEnumModel("b")
print(a < b)
# True

another_a = MyEnumModel("a")
print(a == another_a)
# True
```

### [List Model](./list_model.py)

The `ListModel` is a template for creating new list of some models.
It is a subclass of `RootModel` and provides custom validation and getters for the iterator and items with its index.

```python
from typing import Self

from libraries.models.templates.list_model import ListModel


class MyAscPosIntListModel(ListModel[int]):
    def validate_items(self) -> Self:
        if any(item <= 0 for item in self.root):
            raise ValueError("All items must be positive")
        self.root.sort()
        return self


wrong_lst = MyAscPosIntListModel([3, 0, 6])
# pydantic.ValidationError: All items must be positive

lst = MyAscPosIntListModel([3, 1, 6])
for i in lst:
    print(i)
# 1
# 3
# 6

print(lst[1])
# 3
```

### [String Model](./str_model.py)

The `StrModel` is a template for creating new string models.
It is a subclass of `RootModel` and provides custom validation, equality and alphabetical ordering.

```python
from re import search
from typing import Self

from libraries.models.templates.str_model import StrModel


class MyLowerStrModel(StrModel):
    def validate_str(self) -> Self:
        if not search(r"^[a-z]+$", self.root):
            raise ValueError("Only lowercase alphabets are allowed")
        return self


wrong_str = MyLowerStrModel("123")
# pydantic.ValidationError: Only lowercase alphabets are allowed

str1 = MyLowerStrModel("abc")
str2 = MyLowerStrModel("def")
print(str1 < str2)
# True
```
