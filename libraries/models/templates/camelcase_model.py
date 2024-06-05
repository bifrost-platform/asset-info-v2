from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class CamelCaseModel(BaseModel):
    """A model that converts snake_case to camelCase."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        extra="forbid",
        strict=True,
        str_strip_whitespace=True,
        use_enum_values=True,
        validate_assignment=True,
    )
