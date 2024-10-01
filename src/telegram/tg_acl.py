from typing import List
from src.utils.logger import logger
from telegram.ext.filters import Chat


class ChatACL(Chat):
    __slots__ = ()

    def __init__(self, chat_ids=None, allow_empty: bool = True):
        super().__init__(chat_ids, allow_empty=True)
        self.allow_empty = allow_empty

    def update_acl(self, chats: List[int]):
        chat_set = set()
        if not chats:
            chats = []
        for chat in chats:
            chat_set.add(chat)
        logger.debug(f"{chat_set=}")
        super().add_chat_ids(chat_set)
        logger.info(f"update_acl: Allowed chat IDs: {self.chat_ids}")
        chat_acl_remove = set()
        for chat_id in self.chat_ids:
            if chat_id not in chat_set:
                chat_acl_remove.add(chat_id)
        logger.debug(f"{chat_acl_remove=}")
        super().remove_chat_ids(chat_acl_remove)
        logger.info(f"Chat(s) {chat_acl_remove} removed from access list")
        logger.debug(f"{self.chat_ids=}")


class AdminACL(Chat):
    __slots__ = ()

    def __init__(self, usernames=None, chat_ids=None, allow_empty: bool = False):
        super().__init__(chat_ids, usernames, allow_empty=False)
        self.allow_empty = allow_empty

    def update_acl(self, admins: List[str]):
        logger.debug(f"AdminACLs: {self.chat_ids=}")
        admin_set = set()
        if not admins:
            admins = []
        for admin in admins:
            admin_set.add(admin)
        logger.debug(f"{admin_set=}")
        super().add_usernames(admin_set)
        logger.info(f"update_acl: Admins: {self.usernames}")
        admin_acl_remove = set()
        for admin_username in self.usernames:
            if admin_username not in admin_set:
                admin_acl_remove.add(admin_username)
        logger.debug(f"{admin_acl_remove=}")
        super().remove_usernames(admin_acl_remove)
        logger.info(f"Admin(s) {admin_acl_remove} removed from admin list")
        logger.debug(f"{self.usernames=}")
