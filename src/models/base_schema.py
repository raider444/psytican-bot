from pydantic import BaseModel, ConfigDict
from src.utils.convert import Convert


class BaseEventModel(BaseModel):
    model_config = ConfigDict(
        use_enum_values=True,
        populate_by_name=True,
        alias_generator=Convert.snakecase_camelcase_lower,
        # arbitrary_types_allowed=True
    )
