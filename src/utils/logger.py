import logging
from src.configs.config import settings


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

# logger = logging.getLogger(__name__)
logger = logging.getLogger(name="bookBot")
