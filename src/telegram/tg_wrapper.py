import json
import re
import src.telegram.tg_calendar as Calendar
import src.telegram.common as Common

from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from src.configs.config import settings
from src.google_api.gcalendar import GoogleCalendar
from src.models.calendar.event import CalendarEvent, CalendarDateTime
from src.models.calendar.event_meta import CalendarEventMetadata
from src.telegram.utils import format_calndar_date
from src.utils.logger import logger

# Top-level converstation handler callbacks
ANSWER, CANCEL = map(chr, range(2))
# Calendar  converstation handler
CAL_CONTROL, EDIT_START_DATE, EDIT_END_DATE = map(chr, range(2, 5))
# Event list conversation handler callbacks
GET_EVENTS, EVENT_MENU, DELETE_EVENT, EVENT_CONTROL = map(chr, range(5, 9))
# Event edit conversation handler callbacks
(EVENT_CREATE, EDIT_EVENT, EVENT_SAVE, EVENT_DESC, TYPING, EVENT_EDITOR) = map(
    chr, range(9, 15)
)
# Common callbacks
(CURRENT_EVENT, NEW_EVENT, NEW_EVENT_DICT, BACK, RESTART) = map(chr, range(15, 20))
END = ConversationHandler.END

# Regex patterns
MESSAGE_PATTERNS = r"^([Nn]ew\ event|[Bb]ook|[Бб]ук|[Gg]et\ events)$"
MESSAGE_NEW_EVENT_PATTERNS = r"^([Nn]ew\ event|[Bb]ook|[Бб]ук)$"
MESSAGE_GET_EVENT_PATTERNS = r"^([Gg]et\ events)$"
MESSAGE_CANCEL_PATTERNS = r"^([Cc]ancel|[Ss]top)$"


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    calendars = GoogleCalendar().get_calendars()
    await update.message.reply_text(f"Hello {update.effective_user.first_name}")
    await update.message.reply_text(json.dumps(calendars))
    await update.message.delete()


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    logger.debug(f"{update.callback_query}")
    if update.callback_query:
        user = update.callback_query.from_user
        await update.callback_query.edit_message_text(
            "Bye! I hope we can talk again some day."
        )
    else:
        user = update.message.from_user
        await update.message.reply_text("Bye! I hope we can talk again some day.")
    logger.info("User %s canceled the conversation.", user.first_name)
    context.user_data.pop(NEW_EVENT, None)
    context.user_data.pop(NEW_EVENT_DICT, None)
    context.user_data.pop(CURRENT_EVENT, None)
    return END


async def general_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("You are not allowed to communicate with me")
    logger.info(
        f"User {update.effective_user.username} ({update.effective_user.id}) is not whitelisted"
    )
    return END


async def update_acls(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    Common.update_acl()
    usernames = ",".join(map(str, Common.admin_acl.usernames))
    chats = ",".join(map(str, Common.chat_acl.chat_ids))
    logger.info(f'ACLs updated, admins: "{usernames}", Allowed chats: "{chats}"')
    await update.message.reply_text(
        f'ACLs updated, admins: "{str(usernames)}", Allowed chats: "{chats}"'
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Sends a message with three inline buttons attached."""
    logger.info(
        f'User "{update.effective_user.username}" (ID={update.effective_user.id}) '
        f'started conversation in the chat with ID "{update.effective_chat.id}"'
    )
    # logger.debug(f'{allowed_chats=}')
    keyboard = [["get events", "book", "cancel"]]

    if update.callback_query or update.message.chat.is_forum:
        inline_keyboard = [
            [
                InlineKeyboardButton(text="Get events", callback_data=str(GET_EVENTS)),
                InlineKeyboardButton(
                    text="Create event", callback_data=str(EVENT_CREATE)
                ),
                InlineKeyboardButton(text="Cancel", callback_data=str(CANCEL)),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
    else:
        reply_markup = ReplyKeyboardMarkup(
            keyboard, one_time_keyboard=False, resize_keyboard=True, is_persistent=False
        )
    logger.debug(f"{context.user_data=}")
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            "Hi", parse_mode="HTML", reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            "Hi", parse_mode="HTML", reply_markup=reply_markup
        )
    context.user_data[NEW_EVENT] = True

    return ANSWER


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    await update.message.reply_text("Use /start to test this bot.")


async def calendar_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    logger.info("Using calendar handler")
    logger.debug(f"{context.user_data=}")
    logger.debug(f"{str(EDIT_START_DATE)=}")
    data = update.callback_query.data
    if update.callback_query:
        if data == str(EDIT_START_DATE):
            text = "Select START date: "
            date_event = "start_date"
        elif data == str(EDIT_END_DATE):
            text = "Select END date: "
            date_event = "end_date"
        else:
            text = "Select a date: "
            date_event = "date"
        logger.debug(f"{update.callback_query.data=}")
        context.user_data["date_event"] = date_event
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            text=text, reply_markup=Calendar.create_calendar()
        )
    else:
        await update.message.reply_text(
            text="Select a date: ", reply_markup=Calendar.create_calendar()
        )
    return CAL_CONTROL


def event_list(events: GoogleCalendar) -> list[CalendarEvent]:
    event_matrix = []
    for event in events:
        event_txt = CalendarEvent.model_validate_json(json.dumps(event))
        event_desc = event_txt.description

        row = CalendarEvent(
            id=event_txt.id,
            summary=event_txt.summary,
            start=event_txt.start,
            end=event_txt.end,
            html_link=event_txt.html_link,
        )
        if event_desc:
            pattern = re.compile(r"((\[[^\}]{3,})?\{s*[^\}\{]{3,}?:.*\}([^\{]+\])?)")
            metadata_json = pattern.search(event_desc).group()
            logger.debug(f"{metadata_json=}")
            metadata = CalendarEventMetadata.model_validate_json(metadata_json)
            row.description = metadata
        logger.info(
            f'EVENT: Topic: "{event_txt.summary}" ' f'Date: "{event_txt.start.date}"'
        )
        logger.debug(f"{event_desc=}")
        event_matrix.append(row)
    return event_matrix


async def get_events_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    logger.info(
        f'User "{update.effective_user.username}" (ID={update.effective_user.id} '
        f"requested event list in chat ID={update.effective_chat.id}"
    )
    events = GoogleCalendar().get_events(
        calendar_id=settings.CALENDAR_ID, max_results=settings.EVENTS_PER_LIST
    )
    event_matrix = event_list(events=events)
    context.user_data["event_list"] = event_matrix
    logger.debug(f"{events=}")
    reply_txt = (
        f"Next {settings.EVENTS_PER_LIST} events:\n"
        f"                                                                     "
        f"                                                                 ->\n"
    )
    logger.debug(f"{reply_txt=}")
    keyboard = []
    event_list_text = []
    if len(event_matrix) > 0:
        for event in event_matrix:
            event_link = event.html_link
            logger.debug(f"Keyboard button {event.summary=}, {event_link=}")
            if event.start.date == event.end.date:
                date = event.start.date
            else:
                date = f"{event.start.date}]-[{event.end.date}"
            button_text = f"[{date}]: {event.summary}"
            event_list_text.append(f"<b>[{date}]</b>: {event.summary}")
            logger.debug(f"{event.model_dump_json()=}")
            if (
                update.effective_user.username in Common.admin_acl.usernames
                or event.description
                and event.description.owner["id"] == update.effective_user.id
            ):
                callback_data = str(EVENT_MENU) + event.id
                button_text = "✏️ " + button_text
                row = [
                    InlineKeyboardButton(text=button_text, callback_data=callback_data)
                ]
                keyboard.append(row)
            else:
                logger.warning(
                    f'Event "{event.summary}" does not have metadata '
                    f"probably it was created manually or by older version of this bot"
                )
                callback_data = "IGNORE"
                row = [
                    InlineKeyboardButton(text=button_text, callback_data=callback_data)
                ]
                keyboard.append(row)
        reply_txt = reply_txt + "\n".join(event_list_text)
    else:
        logger.info("No events found in calendar")
        reply_txt = "No upcoming events"

    logger.debug(f"{reply_txt=}")
    logger.debug(f"{update.callback_query=}")
    if update.callback_query:
        keyboard.append([InlineKeyboardButton(text="<< Back", callback_data=END)])
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            text=reply_txt,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML",
        )
    else:
        # this pattern is used for simple messages
        keyboard.append([InlineKeyboardButton(text="Exit", callback_data=CANCEL)])
        await update.message.reply_text(
            reply_txt,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML",
        )

    return EVENT_MENU


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Parses the CallbackQuery and updates the message text."""

    logger.debug(f"{update=}")
    context.user_data["answer"] = update.message.text
    logger.debug(f"{update.message.text=}")

    if re.match(MESSAGE_NEW_EVENT_PATTERNS, update.message.text):
        try:
            context.user_data.pop(CURRENT_EVENT)
        except KeyError as err:
            logger.info(
                f"Context of current event ({str(CURRENT_EVENT)}) is already empety. {err}"
            )
        context.user_data[NEW_EVENT] = True
        logger.info("Creating new event")
        logger.debug(f"{update.message.text=}")
        logger.debug(f"{context.user_data=}")
        return await edit_event(update, context)
    elif re.match(MESSAGE_GET_EVENT_PATTERNS, update.message.text):
        await get_events_handler(update=update, context=context)
    else:
        await update.message.reply_text(f"{update.message.text=}", parse_mode="HTML")


async def inline_calendar_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    query = update.callback_query
    await query.answer()

    selected, date = await Calendar.process_calendar_selection(update, context)
    if selected:
        date_event = context.user_data.get("date_event")
        logger.debug(f"{date_event=}")
        context.user_data[date_event] = date.strftime("%d/%m/%Y")
        formatted_date = format_calndar_date(context.user_data[date_event])
        if context.user_data[NEW_EVENT]:
            if not context.user_data.get(NEW_EVENT_DICT):
                context.user_data[NEW_EVENT_DICT] = {}
            if date_event == "start_date":
                context.user_data[NEW_EVENT_DICT]["start"] = formatted_date
            elif date_event == "end_date":
                context.user_data[NEW_EVENT_DICT]["end"] = formatted_date
            else:
                context.user_data["date"] = date
        else:
            if date_event == "start_date":
                context.user_data[CURRENT_EVENT].start.date = formatted_date
            elif date_event == "end_date":
                context.user_data[CURRENT_EVENT].end.date = formatted_date
            else:
                context.user_data["date"] = date
        logger.debug(f"{context.user_data.get(CURRENT_EVENT)=}")
        await query.edit_message_text(
            text=f'You selected {date_event} {date.strftime("%d/%m/%Y")}',
        )
        logger.debug("{update=}")
        await edit_event(update, context)
    return END


# async def event_description_handler(
#     update: Update, context: ContextTypes.DEFAULT_TYPE
# ) -> str:
#     logger.debug(f"{context.user_data=}")
#     logger.debug(f"{update.message.text=}")
#     context.user_data["event_description"] = update.message.text
#     logger.debug(f'{context.user_data["date"]}')
#     formatted_date = str(
#         datetime.datetime.strptime(context.user_data["date"], "%d/%m/%Y").date()
#     )
#     logger.debug(f"{formatted_date=}")
#     logger.debug(f"{update.effective_user=}")
#     desc = CalendarEventMetadata(
#         owner=update.effective_user.to_dict()
#     ).model_dump_json()
#     logger.debug(f"{desc=}")
#     model_event = CalendarEvent(
#         summary=context.user_data["event_description"],
#         description=desc,
#         start=CalendarDateTime(date=formatted_date),
#         end=CalendarDateTime(date=formatted_date),
#     )
#     logger.debug(f"Event json: {model_event.model_dump_json(exclude_none=True)=}")
#     event = GoogleCalendar().create_event(event=model_event)

#     logger.debug(f"{event=}")
#     logger.info(f'{event["htmlLink"]}')

#     await update.message.reply_text(
#         f'Event with name <b>{context.user_data["event_description"]}</b> created at '
#         f'<b>{context.user_data["date"]}</b> by user <b>{update.effective_user.name}</b>'
#         f"({update.effective_user.link}) .\n"
#         f'<b><a href="{event["htmlLink"]}">Link to event</a></b>',
#         parse_mode="HTML",
#     )

#     return EVENT_DESC


async def end_second_level(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await start(update, context)
    return END


async def end_event_action(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """End gathering of features and return to parent conversation."""
    logger.debug("END EVENT ACTION")
    await get_events_handler(update, context)
    logger.debug("END EVENT ACTION")
    return EVENT_MENU


async def event_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    logger.debug(f"{update.callback_query.data=}")
    logger.debug(f"{context.user_data=}")
    event_id = update.callback_query.data.replace(str(EVENT_MENU), "")
    logger.info(
        f'User "{update.effective_user.id}" (ID={update.effective_user.id}) '
        f'edits event "{event_id}" in chat (ID={update.effective_chat.id})'
    )
    events = context.user_data.get("event_list")
    for evnt in events:
        if evnt.id == event_id:
            logger.debug(f"{evnt=}")
            event: CalendarEvent = evnt
            break
    logger.debug(f"{event=}")
    if event.start.date == event.end.date:
        event_dates = event.start.date
    else:
        event_dates = f"{event.start.date} - {event.end.date}"
    logger.debug(f"{event_dates=}")
    if isinstance(event.description, CalendarEventMetadata):
        if event.description.owner.get("username"):
            event_owner = {
                "text": event.description.owner.get("username"),
                "url": f'https://t.me/{event.description.owner.get("username")}',
                "callback": None,
            }
        else:
            event_owner = {
                "text": f'{event.description.owner["first_name"]} {event.description.owner["last_name"]}',
                "url": None,
                "callback": "NO_ACTION",
            }
    else:
        event_owner = {
            "text": "NO OWNER",
            "url": f"https://t.me/{update.effective_user.username}",
            "callback": None,
        }
    context.user_data[CURRENT_EVENT] = event
    logger.debug(f"INITIALIZED CURRENT EVENT CACHE {context.user_data[CURRENT_EVENT]=}")
    keyboard = [
        [
            InlineKeyboardButton(
                f"{event_dates}: {event.summary}", url=f"{event.html_link}"
            )
        ],
        [
            InlineKeyboardButton(
                f"Created by: @{event_owner['text']}",
                url=event_owner["url"],
                callback_data=event_owner["callback"],
            )
        ],
        [
            InlineKeyboardButton("Edit", callback_data=str(EDIT_EVENT)),
            InlineKeyboardButton("Delete", callback_data=str(DELETE_EVENT)),
        ],
        [
            InlineKeyboardButton("<< Back", callback_data=str(BACK)),
            InlineKeyboardButton("Cancel", callback_data=str(CANCEL)),
        ],
    ]
    event_id = update.callback_query.data.replace(str(EVENT_MENU), "")
    context.user_data[NEW_EVENT] = False
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        text=f"Viewing event {event_id} data:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    context.user_data.pop("event_list")
    return EVENT_CONTROL


async def delete_event(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.debug(f"{context.user_data=}")
    event: CalendarEvent = context.user_data.get(CURRENT_EVENT)
    result = GoogleCalendar().delete_event(event.id)
    if result == "":
        logger.info(f"Event {event.summary} successfully deleted")
        await update.callback_query.edit_message_text(
            f"Event {event.summary} successfully deleted"
        )
    else:
        logger.error(
            f"Event {event.summary} was not deleted by the following reason: {result}"
        )
        await update.callback_query.edit_message_text(
            f"Can't delete event {event.summary}"
        )
    context.user_data.pop(CURRENT_EVENT)
    return CANCEL


async def edit_event(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    logger.debug(f"{context.user_data=}")
    logger.debug(f"{update.callback_query=}")
    buttons = {
        "summary": "Edit summary",
        "start": "Change start date",
        "end": "Change end date",
        "back": "<< Back",
        "callback": RESTART,
        "back_button": InlineKeyboardButton("<< Back", callback_data=str(BACK)),
    }
    if context.user_data.get(NEW_EVENT):
        logger.debug("Before catch exception:")
        buttons["callback"] = RESTART
        # buttons["back"] = "Exit"
        event_dict = context.user_data.get(NEW_EVENT_DICT)
        if not event_dict:
            logger.info("No event dictionary for new event is defined. Error:")
            event_dict = {}
        logger.debug(f"{event_dict=}")
        message = (
            f'New event <b>{event_dict.get("summary", "")}</b>:\n'
            f'<b>Start date</b>: {event_dict.get("start", "undefined")}\n'
            f'<b>End date</b>: {event_dict.get("end", "undefined")}\n'
            f"{event_dict=}"
        )
    else:
        event: CalendarEvent = context.user_data.get(CURRENT_EVENT)
        if isinstance(event.description, CalendarEventMetadata):
            event_owner = f'@{event.description.owner.get("username")}'
        else:
            event_owner = "No owner"
        message = (
            f"Editing event\n<b>Title:</b> {event.summary}\n"
            f"<b>Start date</b>: {event.start.date}\n"
            f"<b>End date</b>: {event.end.date}\n"
            f"<b>Owner</b>: {event_owner}\n"
        )

    keyboard = [
        [
            InlineKeyboardButton(
                f"{buttons.get("summary")}", callback_data=str(EVENT_DESC)
            )
        ],
        [
            InlineKeyboardButton(
                f"{buttons.get("start")}", callback_data=str(EDIT_START_DATE)
            ),
            InlineKeyboardButton(
                f"{buttons.get("end")}", callback_data=str(EDIT_END_DATE)
            ),
        ],
        [
            InlineKeyboardButton(
                buttons.get("back"), callback_data=str(buttons.get("callback"))
            ),
            InlineKeyboardButton("Cancel", callback_data=str(CANCEL)),
            InlineKeyboardButton("Save", callback_data=str(EVENT_SAVE)),
        ],
    ]

    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            text=message, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML"
        )
    # But after we do that, we need to send a new message
    else:
        await update.message.reply_text(
            text=message, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML"
        )

    return EVENT_EDITOR


async def save_event(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.debug(f"{context.user_data=}")
    if context.user_data[NEW_EVENT]:
        action = "created"
        logger.info("Creating new event")
        event_dict = context.user_data.get(NEW_EVENT_DICT, {})
        if not event_dict.get("start"):
            await update.callback_query.edit_message_text("Start date is not defined")
            return END
        logger.debug(f"{event_dict=}")
        desc = CalendarEventMetadata(
            owner=update.effective_user.to_dict()
        ).model_dump_json()
        try:
            event_body = CalendarEvent(
                summary=event_dict.get("summary"),
                description=desc,
                start=CalendarDateTime(date=event_dict.get("start")),
                end=CalendarDateTime(
                    date=event_dict.get("end", event_dict.get("start"))
                ),
            )
        except ValueError as err:
            logger.error(f"{err}")
            error_message_list = []
            for error in err.errors():
                error_message_list.append(f"<b>{str(error['ctx']['error'])}</b>")
            error_message = "\n".join(error_message_list)
            await update.callback_query.answer()
            await update.callback_query.edit_message_text(
                text=error_message, parse_mode="HTML"
            )
            return END
        logger.debug(f"{event_body=}")
        result = GoogleCalendar().create_event(event_body)
    else:
        action = "updated"
        event_body: CalendarEvent = context.user_data.get(CURRENT_EVENT)
        logger.debug(f"{event_body=}")
        try:
            CalendarEvent.model_validate(event_body)
        except ValueError as err:
            logger.error(f"{err}")
            error_message_list = []
            for error in err.errors():
                error_message_list.append(f"<b>{str(error['ctx']['error'])}</b>")
            error_message = "\n".join(error_message_list)
            await update.callback_query.answer()
            await update.callback_query.edit_message_text(
                text=error_message, parse_mode="HTML"
            )
            return END
        event_id = event_body.id
        event_body.id = None
        description = event_body.description
        try:
            event_body.description = description.model_dump_json()
        except AttributeError as err:
            logger.warning(f"Event {event_id} has bad description. Error: {err}")
        logger.debug(f"{event_id=} {event_body=}")
        result = GoogleCalendar().update_event(event_id, event_body)
    logger.debug(f"{result=}")
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        (
            f'Event <a href="'
            f'{result["htmlLink"]}">'
            f"{event_body.summary}</a> "
            f"successfully {action} by "
            f"<b>@{update.effective_user.username}</b>\n"
        ),
        parse_mode="HTML",
        disable_web_page_preview=True,
    )
    context.user_data.pop(NEW_EVENT, None)
    context.user_data.pop(NEW_EVENT_DICT, None)
    context.user_data.pop(CURRENT_EVENT, None)
    return END


async def ask_for_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Prompt user to input data for selected feature."""
    context.user_data["event_description"] = update.callback_query.data
    text = "Type the title of event or booking."

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text)

    return TYPING


async def save_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Save input for feature and return to feature selection."""
    user_data = context.user_data
    logger.debug(f"{user_data=}")
    user_data["event_description"] = update.message.text
    if context.user_data.get(NEW_EVENT):
        if not context.user_data.get(NEW_EVENT_DICT):
            context.user_data[NEW_EVENT_DICT] = {}
        logger.debug(f"{update.message.text=}")
        context.user_data[NEW_EVENT_DICT].update({"summary": update.message.text})
    else:
        user_data[CURRENT_EVENT].summary = update.message.text
    return await edit_event(update, context)


fallback_handlers = [
    CommandHandler("cancel", cancel),
    CommandHandler("start", start),
    MessageHandler(filters.Regex(MESSAGE_CANCEL_PATTERNS), cancel),
    MessageHandler(filters.Regex(MESSAGE_PATTERNS), button),
]

calendar_select_handler = ConversationHandler(
    name="calendar_select",
    conversation_timeout=settings.CONVERSATION_TIMEOUT,
    entry_points=[
        CallbackQueryHandler(
            calendar_handler,
            pattern=("^" + str(EDIT_START_DATE) + "$|^" + str(EDIT_END_DATE) + "$"),
        ),
        CallbackQueryHandler(inline_calendar_handler, pattern="CALENDAR"),
    ],
    states={
        CAL_CONTROL: [
            CallbackQueryHandler(inline_calendar_handler, pattern="CALENDAR"),
        ],
    },
    fallbacks=[
        CommandHandler("cancel", cancel),
        MessageHandler(filters.Regex(MESSAGE_PATTERNS), button),
    ],
    map_to_parent={
        EVENT_EDITOR: EVENT_EDITOR,
        CANCEL: CANCEL,
    },
)

event_editor_handler = ConversationHandler(
    name="event_editor",
    conversation_timeout=settings.CONVERSATION_TIMEOUT,
    entry_points=[
        CallbackQueryHandler(
            edit_event,
            pattern=("^" + str(EDIT_EVENT) + "$|^" + str(EVENT_CREATE) + "$"),
        ),
        MessageHandler(
            filters.Regex(MESSAGE_NEW_EVENT_PATTERNS)
            & (Common.chat_acl | Common.admin_acl),
            button,
            # filters=filters.Regex(MESSAGE_NEW_EVENT_PATTERNS) & Common.chat_acl | Common.admin_acl
        ),
    ],
    states={
        EVENT_EDITOR: [
            CallbackQueryHandler(ask_for_input, pattern="^" + str(EVENT_DESC) + "$"),
            CallbackQueryHandler(save_event, pattern="^" + str(EVENT_SAVE) + "$"),
            calendar_select_handler,
        ],
        TYPING: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_input)],
    },
    fallbacks=fallback_handlers
    + [
        CallbackQueryHandler(cancel, pattern="^" + str(CANCEL) + "$"),
        CallbackQueryHandler(end_event_action, pattern="^" + str(BACK) + "$"),
        CallbackQueryHandler(cancel, pattern="^" + str(END) + "$"),
        CallbackQueryHandler(end_second_level, pattern="^" + str(RESTART) + "$"),
    ],
    map_to_parent={
        CANCEL: CANCEL,
        END: END,
    },
)

event_list_conv_handler = ConversationHandler(
    name="event_list",
    conversation_timeout=settings.CONVERSATION_TIMEOUT,
    entry_points=[
        MessageHandler(
            filters.Regex(MESSAGE_GET_EVENT_PATTERNS)
            & (Common.chat_acl | Common.admin_acl),
            get_events_handler,
        ),
        CallbackQueryHandler(get_events_handler, pattern="^" + str(GET_EVENTS) + "$"),
    ],
    states={
        GET_EVENTS: [
            CallbackQueryHandler(
                get_events_handler, pattern="^" + str(GET_EVENTS) + "$"
            ),
        ],
        EVENT_MENU: [
            CallbackQueryHandler(event_menu_handler, pattern="^" + str(EVENT_MENU)),
        ],
        EVENT_CONTROL: [
            CallbackQueryHandler(delete_event, pattern="^" + str(DELETE_EVENT) + "$"),
            event_editor_handler,
        ],
    },
    fallbacks=fallback_handlers
    + [
        CallbackQueryHandler(end_event_action, pattern="^" + str(BACK) + "$"),
        CallbackQueryHandler(end_second_level, pattern="^" + str(END) + "$"),
        CallbackQueryHandler(cancel, pattern="^" + str(CANCEL) + "$"),
    ],
    map_to_parent={
        # EVENT_EDITOR: EVENT_EDITOR,
        CANCEL: CANCEL,
    },
)

conv_handler = ConversationHandler(
    name="main",
    conversation_timeout=settings.CONVERSATION_TIMEOUT,
    entry_points=[
        CommandHandler(
            "start", start, filters=(Common.chat_acl | Common.admin_acl)
        ),  # Only this works
        # MessageHandler(filters.Regex(r"^(calendar)$"), button),
        event_list_conv_handler,
        event_editor_handler,
    ],
    states={
        ANSWER: [
            event_list_conv_handler,
            event_editor_handler,
        ],
        CANCEL: [CallbackQueryHandler(cancel)],
    },
    fallbacks=fallback_handlers
    + [
        CallbackQueryHandler(cancel, pattern="^" + str(CANCEL) + "$"),
    ],
    # per_message=True,
)
