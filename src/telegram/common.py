# from telegram.ext import filters
from src.telegram.tg_acl import ChatACL, AdminACL
from src.configs.user_conf import yaml_settings
from src.utils.logger import logger

chat_acl = ChatACL(yaml_settings.allowed_chats)
# admin_acl = AdminACL(usernames=yaml_settings.admin_users)
admin_acl = AdminACL(yaml_settings.admin_users)
global_filter = chat_acl | admin_acl


def update_acl():
    yaml_settings.__init__()
    logger.debug(f"{yaml_settings.admin_users=}, {yaml_settings.allowed_chats=}")
    chat_acl.update_acl(
        chats=yaml_settings.allowed_chats,
    )
    admin_acl.update_acl(admins=yaml_settings.admin_users)
