from prometheus_client import Info


tg_app_info = Info("bot", "Ingormation about TG_BOT")
tg_app_info.info(
    {
        "major_version": "0.0.0",
        "architecture": "monolith",
    }
)
