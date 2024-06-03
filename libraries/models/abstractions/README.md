# Models.Abstractions

This library contains abstracted models for creating new models.

## Table of Contents

- [Models.Abstractions](#modelsabstractions)
    - [Table of Contents](#table-of-contents)
    - [List of Abstractions](#list-of-abstractions)
        - [Enum Type Model](#enum-type-model)

## List of Abstractions

### [Enum Type Model](../abstractions/enum_type_model.py)

This abstraction is dependent on the below models:

- [`libraries.models.enum_info_list`](../enum_info_list.py)
- [`libraries.models.templates.enum_model`](../templates/enum_model.py)

The `EnumTypeModel` is an abstracted class for creating new enum type models.
It is a subclass of [`EnumModel`](../templates/enum_model.py) and provides custom validation and getters for the path to
the enum files and the enum info list.

See the [`EnumTypeId`](../terminals/enum_type_id.py) and [`EnumTypeTag`](../terminals/enum_type_tag.py) for examples.

### [Information Model](./info_model.py)

This abstraction is dependent on the below models:

- [`libraries.models.id`](../terminals/id.py)
- [`libraries.models.image_info`](../image_info.py)
- [`libraries.models.info_category`](../terminals/info_category.py)
- [`libraries.models.tag_list`](../terminals/tag_list.py)

The `InfoModel` is an abstracted class for creating new info models.
It is a subclass of [`CamelCaseModel`](../templates/camelcase_model.py) and provides essential properties and getters
for the models.
