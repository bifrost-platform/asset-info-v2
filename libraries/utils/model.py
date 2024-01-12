from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class CamelCaseModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        extra="forbid",
        strict=True,
        str_strip_whitespace=True,
        str_min_length=1,
        use_enum_values=True,
        validate_assignment=True
    )
