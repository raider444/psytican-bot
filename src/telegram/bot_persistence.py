from redis import Redis
from telegram.ext import PicklePersistence
from pydantic import RedisDsn
from src.configs.config import settings, BotPersistence
from src.telegram.redispesistence import RedisPersistence


def bot_persistense_config(persistence: BotPersistence):
    if persistence == "file":
        bot_persistence = PicklePersistence(
            filepath=settings.PERSISTENCE.FILE, update_interval=0
        )
    elif persistence == "redis":
        redis_dsn: RedisDsn = settings.REDIS_DSN.get_secret_value()
        redis_instance = Redis(
            host=redis_dsn.host,
            port=redis_dsn.port,
            db=redis_dsn.path[1:],
            password=redis_dsn.password,
        )
        bot_persistence = RedisPersistence(redis=redis_instance, update_interval=0)
    else:
        bot_persistence = None
    return bot_persistence
