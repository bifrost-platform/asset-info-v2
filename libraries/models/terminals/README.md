# Models.Terminals

This library contains terminal models for creating new models.
The modules on this library are dependent on the [`Models.Templates`](../templates), [`Models.Terminals`](.) and some
kinds of [`Models.Abstractions`](../abstractions) modules which are dependent on the
only [`Models.Templates`](../templates) and [`Models.Terminals`](.).

## Table of Contents

- [Models.Terminals](#modelsterminals)
    - [Table of Contents](#table-of-contents)
    - [List of Terminals](#list-of-terminals)
        - [Address](./address.py)
            - [EVM Address](./address_evm.py)
        - [Description](./description.py)
        - [Engine](./engine.py)
        - [Enum Type Models](../abstractions/enum_type_model.py)
            - [Enum Type Id](./enum_type_id.py)
            - [Enum Type Tag](./enum_type_tag.py)
        - [ID](./id.py)
            - [ID List](./id_list.py)
        - [Image Type](./image_type.py)
        - [Info Category](./info_category.py)
        - [Network Type](./network_type.py)
        - [Tag](./tag.py)
            - [Tag List](./tag_list.py)

## List of Terminals

### [Address](./address.py)

This module contains the `Address` model for creating new address models.
Address models are representations of addresses in the blockchain.
It is a union of the [`AddressEVM`](./address_evm.py) only (for now).

#### [EVM Address](./address_evm.py)

This module contains the `AddressEVM` model for creating new EVM address value.
`AddressEVM` model is a subclass of [`StrModel`](../templates/str_model.py) and provides a checksum validation and
comparison.

### [Description](./description.py)

This module contains the `Description` model for creating new description value.
`Description` model is a subclass of [`StrModel`](../templates/str_model.py) and provides a description validation.

### [Engine](./engine.py)

This module contains the `Engine` model for creating new engine enum value.
`Engine` model is a subclass of [`EnumModel`](../templates/enum_model.py) provides value checkers.

### [Enum Type Models](../abstractions/enum_type_model.py)

Below are the concrete models of the [`EnumTypeModel](../abstractions/enum_type_model.py) abstraction.

#### [Enum Type Id](./enum_type_id.py)

This module contains the `EnumTypeId` model for creating a new ID enum value.
`EnumTypeId` model is a subclass of [`EnumTypeModel`](../abstractions/enum_type_model.py) and provides its constructors.

#### [Enum Type Tag](./enum_type_tag.py)

This module contains the `EnumTypeTag` model for creating a new tag enum value.
`EnumTypeTag` model is a subclass of [`EnumTypeModel`](../abstractions/enum_type_model.py) and provides its
constructors.

### [ID](./id.py)

This module contains the `ID` model for creating new ID value.
`ID` model is a subclass of [`StrModel`](../templates/str_model.py) and provides an ID validation.

#### [ID List](./id_list.py)

This module contains the `IDList` model for creating new ID list value.
`IDList` model is a subclass of [`ListModel`](../templates/list_model.py) and provides an ID list validation.

### [Image Type](./image_type.py)

This module contains the `ImageType` model for creating new image type enum value.
`ImageType` model is a subclass of [`EnumModel`](../templates/enum_model.py) and provides value checkers and utils.

### [Info Category](./info_category.py)

This module contains the `InfoCategory` model for creating new info category enum value.
`InfoCategory` model is a subclass of [`EnumModel`](../templates/enum_model.py) and provides constructors, value
checkers and utils.

### [Network Type](./network_type.py)

This module contains the `NetworkType` model for creating new network type enum value.
`NetworkType` model is a subclass of [`EnumModel`](../templates/enum_model.py) and provides value checkers.

### [Tag](./tag.py)

This module contains the `Tag` model for creating new tag value.
`Tag` model is a subclass of [`StrModel`](../templates/str_model.py) and provides a tag validation.

#### [Tag List](./tag_list.py)

This module contains the `TagList` model for creating new tag list value.
`TagList` model is a subclass of [`ListModel`](../templates/list_model.py) and provides a tag list validation.
