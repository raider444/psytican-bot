from prometheus_client import Info
from importlib.metadata import version


tg_app_info = Info("bot", "Ingormation about TG_BOT")
tg_app_info.info(
    {
        "major_version": version("psytican-bot"),
        "architecture": "monolith",
    }
)
