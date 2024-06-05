# Models

This library contains models for creating new models.
The modules on this library are dependent on the [`CamelCaseModel`](./templates/camelcase_model.py) directly or
indirectly.

## Table of Contents

- [Models](#models)
    - [Table of Contents](#table-of-contents)
    - [List of Models](#list-of-models)
        - [Info Models](./abstractions/info_model.py)
            - [Asset](./asset.py)
            - [Network](./network.py)
            - [Protocol](./protocol.py)
        - [Contract](./contract.py)
            - [Contract List](./contract_list.py)
        - [Currency](./currency.py)
        - [Reference](./reference.py)
            - [Reference List](./reference_list.py)

## List of Models

### [Info Models](./abstractions/info_model.py)

Below are the concrete models of the [`InfoModel`](./abstractions/info_model.py) abstraction.

#### [Asset](./asset.py)

This module contains the `Asset` model for creating new asset models.
`Asset` models are representations of assets in the blockchain.
The items are stored in the [assets'](../../assets) directory.

#### [Network](./network.py)

This module contains the `Network` model for creating new network models.
`Network` models are representations of networks in the blockchain.
The items are stored in the [networks'](../../networks) directory.

#### [Protocol](./protocol.py)

This module contains the `Protocol` model for creating new protocol models.
`Protocol` models are representations of protocols in the blockchain.
The items are stored in the [protocols'](../../protocols) directory.

### [Contract](./contract.py)

This module contains the `Contract` model for creating new contract models.
`Contract` model is a component of the `Asset` model and represents the contract of the asset.

#### [Contract List](./contract_list.py)

This module contains the `ContractList` model for creating new contract list models.
`ContractList` model is a list of `Contract` models.

### [Currency](./currency.py)

This module contains the `Currency` model for creating new currency models.
`Currency` model is a component of the `Network` model and represents the currency of the network.

### [Reference](./reference.py)

This module contains the `Reference` model for creating new reference models.
`Reference` model is a component of the `Asset` and `Network` models and represents the references of each model.

#### [Reference List](./reference_list.py)

This module contains the `ReferenceList` model for creating new reference list models.
`ReferenceList` model is a list of `Reference` models.
