from src.configs.user_conf import yaml_settings
from src.utils.logger import logger
from telegram.ext.filters import Chat

# allowed_chats: Chat = filters.Chat(chat_acl())


class ChatACL(Chat):
    # __slots__ = ()

    def __init__(self, chat_ids=None):
        super().__init__(chat_ids)

    # def __init__(
    #         self,
    #         chat_ids: Optional[Set[str]] = None
    #     ):
    #     super().__init__(chat_ids)
    #     self.chat_ids = self.update_acl()
    #     logger.info(f'Allowed chat IDs: {self.chat_ids}')
    #     # chat_ids: Set[int] = set()
    #     # chat_usernames = Set[str] = set()

    def update_acl(self):  # TODO Make list of chat parametrized
        yaml_settings.__init__
        admin_list = yaml_settings.admin_users if yaml_settings.admin_users else []
        logger.debug(f"{admin_list=}")
        group_list = yaml_settings.allowed_chats if yaml_settings.allowed_chats else []
        logger.debug(f"{group_list=}")
        chat_acl = admin_list + group_list
        logger.debug(f"{chat_acl=}")
        chat_acl_set = {chat for chat in chat_acl}
        super().add_chat_ids(chat_acl_set)
        logger.info(f"update_acl: Allowed chat IDs: {self.chat_ids}")
        chat_acl_remove = set()
        for chat_id in chat_acl_set:
            if chat_id not in chat_acl:
                chat_acl_remove.add(chat_id)
        logger.debug(f"{chat_acl_remove=}")
        super().remove_chat_ids(chat_acl_remove)
        logger.info(f"Chat(s) {chat_acl_remove} removed from access list")
        logger.debug(f"{self.chat_ids=}")
