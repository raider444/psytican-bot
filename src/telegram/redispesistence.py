import pickle
import inspect
import logging
from collections import defaultdict
from copy import deepcopy
from typing import Any, DefaultDict, Dict, Optional, Tuple, Union, cast
from redis import Redis
from redis.exceptions import ConnectionError

from telegram.ext import BasePersistence, PersistenceInput, ContextTypes
from telegram.ext._utils.types import ConversationDict, UD, CD, CDCData, BD

logger = logging.getLogger(__name__)


class RedisPersistence(BasePersistence):
    """Using Redis to make the bot persistent"""

    def __init__(
        self,
        redis: Redis,
        on_flush: bool = False,
        store_data: PersistenceInput = None,
        update_interval: float = 60,
        context_types: ContextTypes[Any, UD, CD, BD] = None,
    ):
        super().__init__(store_data=store_data, update_interval=update_interval)
        self.redis: Redis = redis
        self.on_flush: Optional[bool] = on_flush
        self.user_data: Optional[Dict[int, UD]] = None
        self.chat_data: Optional[Dict[int, CD]] = None
        self.bot_data: Optional[BD] = None
        self.callback_data: Optional[CDCData] = None
        self.conversations: Optional[
            Dict[str, Dict[Tuple[Union[int, str], ...], object]]
        ] = None
        self.context_types: ContextTypes[Any, UD, CD, BD] = cast(
            ContextTypes[Any, UD, CD, BD], context_types or ContextTypes()
        )

    async def load_redis(self) -> None:
        try:
            get_tg_bot_presistence = self.redis.get("TelegramBotPersistence")
        except ConnectionError as err:
            logger.error(
                f"Redis is unavailable, bot persistence is disabled. "
                f"ConnectionError: {err}"
            )
            raise TypeError("Failed to connect to Redis") from err
        try:
            if inspect.iscoroutinefunction(get_tg_bot_presistence):
                data_bytes = await get_tg_bot_presistence
            else:
                data_bytes = get_tg_bot_presistence
            if data_bytes:
                data = pickle.loads(data_bytes)
                self.user_data = defaultdict(dict, data["user_data"])
                self.chat_data = defaultdict(dict, data["chat_data"])
                # For backwards compatibility with files not containing bot data
                self.bot_data = data.get("bot_data", {})
                self.callback_data = data.get("callback_data", {})
                self.conversations = data["conversations"]
            else:
                self.conversations = {}
                self.user_data = {}
                self.chat_data = {}
                self.bot_data = self.context_types.bot_data()
                self.callback_data = None
        except Exception as exc:
            raise TypeError("Something went wrong unpickling from Redis") from exc

    def dump_redis(self) -> None:
        data = {
            "conversations": self.conversations,
            "callback_data": self.callback_data,
            "user_data": self.user_data,
            "chat_data": self.chat_data,
            "bot_data": self.bot_data,
        }
        data_bytes = pickle.dumps(data)
        try:
            self.redis.set("TelegramBotPersistence", data_bytes)
        except ConnectionError as err:
            logger.error(
                f"Redis is unavailable, bot persistence is disabled. "
                f"ConnectionError: {err}"
            )

    async def get_user_data(self) -> DefaultDict[int, Dict[Any, Any]]:
        """Returns the user_data from the pickle on Redis if it exists or an empty :obj:`defaultdict`."""
        if self.user_data:
            pass
        else:
            await self.load_redis()
        return deepcopy(self.user_data)  # type: ignore[arg-type]

    async def get_chat_data(self) -> DefaultDict[int, Dict[Any, Any]]:
        """Returns the chat_data from the pickle on Redis if it exists or an empty :obj:`defaultdict`."""
        if self.chat_data:
            pass
        else:
            await self.load_redis()
        return deepcopy(self.chat_data)  # type: ignore[arg-type]

    async def get_bot_data(self) -> Dict[Any, Any]:
        """Returns the bot_data from the pickle on Redis if it exists or an empty :obj:`dict`."""
        if self.bot_data:
            pass
        else:
            await self.load_redis()
        return deepcopy(self.bot_data)  # type: ignore[arg-type]

    async def get_conversations(self, name: str) -> ConversationDict:
        """Returns the conversations from the pickle on Redis if it exsists or an empty dict."""
        if self.conversations:
            pass
        else:
            await self.load_redis()
        return self.conversations.get(name, {}).copy()  # type: ignore[union-attr]

    async def update_conversation(
        self, name: str, key: Tuple[int, ...], new_state: Optional[object]
    ) -> None:
        """Will update the conversations for the given handler and depending
        on :attr:`on_flush` save the pickle on Redis."""
        if not self.conversations:
            self.conversations = dict()
        if self.conversations.setdefault(name, {}).get(key) == new_state:
            return
        self.conversations[name][key] = new_state
        if not self.on_flush:
            self.dump_redis()

    async def update_user_data(self, user_id: int, data: Dict) -> None:
        """Will update the user_data and depending on :attr:`on_flush` save the pickle on Redis."""
        if self.user_data is None:
            self.user_data = defaultdict(dict)
        if self.user_data.get(user_id) == data:
            return
        self.user_data[user_id] = data
        if not self.on_flush:
            self.dump_redis()

    async def update_chat_data(self, chat_id: int, data: Dict) -> None:
        """Will update the chat_data and depending on :attr:`on_flush` save the pickle on Redis."""
        if self.chat_data is None:
            self.chat_data = defaultdict(dict)
        if self.chat_data.get(chat_id) == data:
            return
        self.chat_data[chat_id] = data
        if not self.on_flush:
            self.dump_redis()

    async def update_bot_data(self, data: Dict) -> None:
        """Will update the bot_data and depending on :attr:`on_flush` save the pickle on Redis."""
        if self.bot_data == data:
            return
        self.bot_data = data.copy()
        if not self.on_flush:
            self.dump_redis()

    async def flush(self) -> None:
        """Will save all data in memory to pickle on Redis."""
        self.dump_redis()

    async def drop_chat_data(self, chat_id: int) -> None:
        """Will delete the specified key from the ``chat_data`` and save the pickle file.
        Args:
            chat_id (:obj:`int`): The chat id to delete from the persistence.
        """
        if self.chat_data is None:
            return
        self.chat_data[chat_id] = None

        if not self.on_flush:
            self.dump_redis()

    async def drop_user_data(self, user_id: int) -> None:
        """Will delete the specified key from the ``user_data`` and save the pickle on Redis.
        Args:
            user_id (:obj:`int`): The user id to delete from the persistence.
        """
        if self.user_data is None:
            return
        self.user_data[user_id] = None

        if not self.on_flush:
            self.dump_redis()

    async def get_callback_data(self) -> Optional[CDCData]:
        """Returns the callback data from the pickle file if it exists or :obj:`None`.

        Returns:
            Tuple[List[Tuple[:obj:`str`, :obj:`float`, Dict[:obj:`str`, :class:`object`]]],
            Dict[:obj:`str`, :obj:`str`]] | :obj:`None`: The restored metadata or :obj:`None`,
            if no data was stored.
        """
        if self.callback_data:
            pass
        else:
            await self.load_redis()
        if self.callback_data is None:
            return None
        return deepcopy(self.callback_data)

    async def refresh_bot_data(self, bot_data: BD) -> None:
        """Does nothing."""

    async def refresh_chat_data(self, chat_id: int, chat_data: CD) -> None:
        """Does nothing."""

    async def refresh_user_data(self, user_id: int, user_data: UD) -> None:
        """Does nothing."""

    async def update_callback_data(self, data: CDCData) -> None:
        """Will update the callback_data (if changed) and save the pickle on Redis.
        Args:
            data (Tuple[List[Tuple[:obj:`str`, :obj:`float`, \
                Dict[:obj:`str`, :class:`object`]]], Dict[:obj:`str`, :obj:`str`]]):
                The relevant data to restore :class:`telegram.ext.CallbackDataCache`.
        """
        if self.callback_data == data:
            return
        self.callback_data = data
        if not self.on_flush:
            self.dump_redis()
