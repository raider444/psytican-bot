import asyncio
import uvicorn.server
import src.telegram.tg_wrapper as TgHandlers
import uvicorn
import src.telegram.common as Common

from contextlib import asynccontextmanager
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from starlette_prometheus import metrics, PrometheusMiddleware
from http import HTTPStatus
from importlib.metadata import version

from src.configs.config import settings
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


app = FastAPI(lifespan=lifespan, version=version("psytican-bot"))

app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics/", metrics, name="metrics", include_in_schema=True)


@app.post("/")
async def process_update(request: Request):
    req = await request.json()
    logger.debug(f"{req=}")
    update = Update.de_json(req, tg_app.bot)
    await tg_app.process_update(update)
    return Response(status_code=HTTPStatus.OK)


@app.get("/healthz")
async def healthz(request: Request):
    response = {"version": version("psytican-bot"), "status": "ok"}
    return JSONResponse(
        content=response,
    )


@app.get("/metric")
async def metric(request: Request):
    return metrics(request)


@app.patch("/update_acls")
async def update_acls(request: Request):
    Common.update_acl()
    return Response(
        status_code=HTTPStatus.NO_CONTENT,
    )


tg_app = (
    ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN.get_secret_value()).build()
)


tg_app.add_handler(TgHandlers.conv_handler)
tg_app.add_handler(CommandHandler("start", TgHandlers.general_start))
tg_app.add_handler(CommandHandler("hello", TgHandlers.hello))
tg_app.add_handler(CommandHandler("help", TgHandlers.help_command))
tg_app.add_handler(CommandHandler("cancel", TgHandlers.cancel))
tg_app.add_handler(
    CommandHandler("update_acls", TgHandlers.update_acls, filters=Common.admin_acl)
)


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
