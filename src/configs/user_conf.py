from src.configs.config import settings
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)
from src.utils.convert import Convert


class YamlSettings(BaseSettings):
    TEST_STUFF: str = ""
    admin_users: list[str] | None = None
    allowed_chats: list[int] | None = None

    model_config: SettingsConfigDict = {
        "yaml_file": settings.YAML_CONFIG_PATH,
        "alias_generator": Convert.snakecase_camelcase_lower,
    }

    @classmethod
    def settings_customise_sources(  # noqa
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (YamlConfigSettingsSource(settings_cls),)


yaml_settings = YamlSettings()
