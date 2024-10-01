import os

from pathlib import Path
from pydantic import Field, SecretStr, HttpUrl
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)
from pydantic_vault import VaultSettingsSource


class Settings(BaseSettings):
    LOG_LEVEL: str = "DEBUG"
    CONVERSATION_TIMEOUT: float = 300
    EVENTS_PER_LIST: int = 20
    PORT: int = 8000
    SCOPES: list = ["https://www.googleapis.com/auth/calendar"]
    CALENDAR_ID: str = "your_gcal_id@group.calendare.google.com"
    VAULT_SECRET_PATH: str = "secret/data/path/to/secret"
    YAML_CONFIG_PATH: Path = "../config.yaml"
    GOOGLE_CLIENT_CONFIG: SecretStr = Field(
        ...,
        json_schema_extra={
            "vault_secret_path": os.getenv("VAULT_SECRET_PATH", VAULT_SECRET_PATH),
            "vault_secret_key": "GOOGLE_CLIENT_CONFIG",
        },
    )
    TELEGRAM_BOT_TOKEN: SecretStr = Field(
        ...,
        json_schema_extra={
            "vault_secret_path": os.getenv("VAULT_SECRET_PATH", VAULT_SECRET_PATH),
            "vault_secret_key": "TELEGRAM_BOT_TOKEN",
        },
    )
    WEBHOOK_MODE: bool = False
    WEBHOOK_URL: HttpUrl = "https://tg-bot.psynet.su/"
    WEBHOOK_SECRET: SecretStr = Field(
        ...,
        json_schema_extra={
            "vault_secret_path": os.getenv("VAULT_SECRET_PATH", VAULT_SECRET_PATH),
            "vault_secret_key": "WEBHOOK_SECRET",
        },
    )

    model_config: SettingsConfigDict = {
        "case_sensitive": True,
        "vault_url": os.getenv("VAULT_URL"),
        "vault_kubernetes_role": os.getenv("VAULT_KUBERNETES_ROLE", None),
        "vault_token": os.getenv("VAULT_TOKEN", None),
        "vault_auth_mount_point": os.getenv("VAULT_AUTH_MOUNT_POINT", None),
        "vault_namespace": os.getenv("VAULT_NAMESPACE", None),
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
        # This is where you can choose which settings sources to use and their priority
        if "VAULT_URL" in os.environ:
            return (
                init_settings,
                env_settings,
                dotenv_settings,
                VaultSettingsSource(settings_cls),
                file_secret_settings,
            )
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            # VaultSettingsSource(settings_cls),
            file_secret_settings,
        )


settings = Settings()
