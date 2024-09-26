import asyncio
import uvicorn.server
import src.telegram.tg_wrapper as TgHandlers
import uvicorn

from contextlib import asynccontextmanager
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler
from fastapi import FastAPI, Request, Response
from starlette_prometheus import metrics, PrometheusMiddleware
from http import HTTPStatus

from src.config import settings
from src.utils.logger import logger


@asynccontextmanager
async def lifespan(_: FastAPI):
    if settings.WEBHOOK_MODE:
        logger.info(f"Running in webhook mode, webhook url: {settings.WEBHOOK_URL}")
        await tg_app.bot.setWebhook(
            url=str(settings.WEBHOOK_URL),
            secret_token=settings.WEBHOOK_SECRET.get_secret_value(),
        )  # replace <your-webhook-url>
        async with tg_app:
            await tg_app.start()
            yield
            await tg_app.stop()
    else:
        logger.info("Running in polling mode")
        await tg_app.bot.deleteWebhook()
        async with tg_app:
            await tg_app.updater.start_polling()
            await tg_app.start()
            yield
            await tg_app.updater.stop()
            await tg_app.stop()


app = FastAPI(lifespan=lifespan)

app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics/", metrics, name="metrics", include_in_schema=True)


@app.post("/")
async def process_update(request: Request):
    req = await request.json()
    update = Update.de_json(req, tg_app.bot)
    await tg_app.process_update(update)
    return Response(status_code=HTTPStatus.OK)


@app.get("/metric")
async def metric(request: Request):
    return metrics(request)


tg_app = (
    ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN.get_secret_value()).build()
)


tg_app.add_handler(TgHandlers.conv_handler)
tg_app.add_handler(CommandHandler("start", TgHandlers.start))
tg_app.add_handler(CommandHandler("hello", TgHandlers.hello))
tg_app.add_handler(CommandHandler("help", TgHandlers.help_command))
tg_app.add_handler(CommandHandler("cancel", TgHandlers.cancel))


async def run_bot() -> None:
    logger.debug(" ---------------------> Debug logging")

    from src.metrics.bot_info_metrics import tg_app_info  # noqa

    server = uvicorn.Server(
        config=uvicorn.Config(
            "src.main:app",
            port=int(settings.PORT),
            host="0.0.0.0",
            reload=True,
            log_config=None,
        )
    )

    async with tg_app:
        await server.serve()


def main():
    asyncio.run(run_bot())


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Application stopped")
