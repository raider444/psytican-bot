import logging
from src.configs.config import settings


class EndpointFilter(logging.Filter):
    def __init__(self, name: str = "", endpoint: str = "") -> None:
        super().__init__(name)
        self.endpoint: str = endpoint

    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find(self.endpoint) == -1


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(module)s: %(message)s",
    level=settings.LOG_LEVEL,
    # format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=settings.LOG_LEVEL
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.INFO)
logging.getLogger("telegram.ext").setLevel(logging.INFO)
logging.getLogger("telegram.ext.ConversationHandler").setLevel(logging.INFO)
logging.getLogger("apscheduler.scheduler").setLevel(logging.INFO)
logging.getLogger("oauth2client").setLevel(logging.INFO)
logging.getLogger("pydantic-vault").setLevel(logging.DEBUG)
logging.getLogger("uvicorn.access").addFilter(EndpointFilter(endpoint="/healthz"))
logging.getLogger("uvicorn.access").addFilter(EndpointFilter(endpoint="/metrics"))
logging.getLogger("uvicorn.access").addFilter(EndpointFilter(endpoint="/metrics/"))

# logger = logging.getLogger(__name__)
logger = logging.getLogger(name="bookBot")
