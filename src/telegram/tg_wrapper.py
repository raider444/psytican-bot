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
from src.utils.convert import DATE_PATTERN, DateParser

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
MESSAGE_NEW_EVENT_GRREDY_PATTERNS = r"^([Nn]ew\ event|[Bb]ook|[Бб]ук)"
MESSAGE_NEW_EVENT_PATTERNS = MESSAGE_NEW_EVENT_GRREDY_PATTERNS + "$"
MESSAGE_GET_EVENT_PATTERNS = r"^([Gg]et\ events)$"
MESSAGE_PATTERNS = MESSAGE_NEW_EVENT_PATTERNS + "|" + MESSAGE_GET_EVENT_PATTERNS
MESSAGE_CANCEL_PATTERNS = r"^([Cc]ancel|[Ss]top)$"


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    calendars = GoogleCalendar().get_calendars()
    await update.message.reply_text(
        f"Hello {update.effective_user.first_name}",
        disable_notification=settings.DISABLE_NOTIFICATION,
    )
    await update.message.reply_text(json.dumps(calendars))
    await update.message.delete()


async def fast_book(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    usage_text: str = (
        "\n<b>Usage:\n</b>"
        "<code>book &lt;start_date&gt;[-&lt;end_date&gt;]: &lt;Event description&gt;</code>\n"
        "Everything in &lt;&gt; brackets is mandatory, in [] brackets is optional.\n "
        "if &lt;end date&gt; is not defined event end date will be equal it's start date.\n"
        "<b>Examples:</b>\n"
        '"<code>book 22.11: My awesome event</code>" will create the event at 24 of '
        "November this year\n"
        '"<code>бук 22.11-23.11: 2 Саба 2 верха</code>" will create the event 22 to 23 of '
        "November this year\n"
        '"<code>бук 22.11.2024: 2 Саба 2 верха</code>" will create the event 22 November 2024\n'
    )
    logger.debug(update.message.text)
    date_pattern = DATE_PATTERN
    regex = re.compile(
        MESSAGE_NEW_EVENT_GRREDY_PATTERNS
        + r"\s+("
        + date_pattern
        + r")(?:-("
        + date_pattern
        + r")?)?\:?\s*(.*)$"
    )
    logger.debug(f"{regex=}, {regex.groups=}, {regex.pattern=}, {regex.flags=}")
    matching = regex.match(update.message.text)
    if not matching:
        await update.message.reply_text(
            text="<b>Incorrect booking request</b>\n" + usage_text,
            parse_mode="HTML",
            disable_notification=settings.DISABLE_NOTIFICATION,
        )
        return END
    param_list = regex.findall(update.message.text)[0]
    logger.debug(f"{matching=}, {param_list=}")
    index_act = 0
    index_start_date = 1
    index_end_date = 5
    index_description = 9
    action = param_list[index_act]
    try:
        start_date = DateParser.parse_date(param_list[index_start_date])
    except ValueError as err:
        logger.error(f"Bad start date. Error: {err}")
        await update.message.reply_text(
            text=f'<b>"{param_list[index_start_date]}" is incorrect start date.</b>\n'
            + usage_text,
            parse_mode="HTML",
            disable_notification=settings.DISABLE_NOTIFICATION,
        )
        return END
    if not param_list[index_end_date]:
        end_date = start_date
    else:
        try:
            end_date = DateParser.parse_date(param_list[index_end_date])
        except ValueError as err:
            logger.error(f"Bad end date. Error: {err}")
            await update.message.reply_text(
                text=f'<b>"{param_list[index_end_date]}" is incorrect end date</b>\n'
                + usage_text,
                parse_mode="HTML",
                disable_notification=settings.DISABLE_NOTIFICATION,
            )
            return END
    if not param_list[index_description]:
        logger.error("Event description not defined")
        await update.message.reply_text(
            text="<b>You must define the event summary.</b>\n" + usage_text,
            parse_mode="HTML",
            disable_notification=settings.DISABLE_NOTIFICATION,
        )
        return END
    description = param_list[index_description]
    logger.info(
        f'Creating event... Action: "{action}". Start date: "{start_date}". '
        f'End date: "{end_date}". Description: "{description}"'
    )
    context.user_data[NEW_EVENT] = True
    context.user_data[NEW_EVENT_DICT] = {
        "summary": description,
        "start": start_date,
        "end": end_date,
    }
    logger.info(
        f'Event "{context.user_data[NEW_EVENT_DICT]["summary"]}" which will be '
        f' held from {context.user_data[NEW_EVENT_DICT]["summary"]} to '
        f'{context.user_data[NEW_EVENT_DICT]["summary"]} is being created'
    )
    logger.debug(f"{context.user_data[NEW_EVENT_DICT]=}")
    return await save_event(update=update, context=context)


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
        await update.message.reply_text(
            "Bye! I hope we can talk again some day.",
            disable_notification=settings.DISABLE_NOTIFICATION,
        )
    logger.info(f"User {user.first_name} (ID={user.id}) canceled the conversation.")
    context.user_data.pop(NEW_EVENT, None)
    context.user_data.pop(NEW_EVENT_DICT, None)
    context.user_data.pop(CURRENT_EVENT, None)
    return END


async def general_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("You are not allowed to communicate with me")
    logger.info(
        f"User {update.effective_user.username} ({update.effective_user.id}) is not whitelisted. "
        f"Chat ID={update.effective_chat.id}"
    )
    return END


async def update_acls(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    Common.update_acl()
    usernames = ",".join(map(str, Common.admin_acl.usernames))
    chats = ",".join(map(str, Common.chat_acl.chat_ids))
    logger.info(
        f'ACLs updated, admins: "{usernames}", Allowed chats: "{chats}" '
        f'by user "{update.effective_user.username}" (ID={update.effective_user.id})'
    )
    await update.message.reply_text(
        f'ACLs updated, admins: "{str(usernames)}", Allowed chats: "{chats}"',
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
            "Hi",
            parse_mode="HTML",
            reply_markup=reply_markup,
        )
    else:
        await update.message.reply_text(
            "Hi",
            parse_mode="HTML",
            reply_markup=reply_markup,
            disable_notification=settings.DISABLE_NOTIFICATION,
        )
    context.user_data[NEW_EVENT] = True

    return ANSWER


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    await update.message.reply_text(
        "Use /start to test this bot.",
        disable_notification=settings.DISABLE_NOTIFICATION,
    )


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
            text="Select a date: ",
            reply_markup=Calendar.create_calendar(),
            disable_notification=settings.DISABLE_NOTIFICATION,
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
        f'User "{update.effective_user.username}" (ID={update.effective_user.id}) '
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
            try:
                if event.description.owner.get("username"):
                    event_owner = {
                        "name": event.description.owner.get("username"),
                        "link": f'<a href="https://t.me/'
                        f"""{event.description.owner.get('username')}">"""
                        f"{event.description.owner.get('username')}</a>",
                    }
                else:
                    event_owner_raw = (
                        f"{event.description.owner.get('first_name')} "
                        f"{event.description.owner.get('last_name')}"
                        # f"ID: {event.description.owner.get('id')}"
                    )
                    event_owner = {"name": event_owner_raw, "link": event_owner_raw}
            except AttributeError as err:
                logger.warning(
                    f"Event {event.summary} with ID={event.id} was probably "
                    f"created manually of incorrectly. Error message {err}"
                )
                event_owner = {"name": "unknown", "link": "unknown"}
            button_text = f"[{date}]: {event.summary} ({event_owner.get("name")})"
            event_list_text.append(
                f"<b>[{date}]</b>: {event.summary} ({event_owner.get("link")})"
            )
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
                row = [InlineKeyboardButton(text=button_text, url=event_link)]
                keyboard.append(row)
        reply_txt = reply_txt + "\n".join(event_list_text)
    else:
        logger.info("No events found in calendar")
        reply_txt = "No upcoming events"

    logger.debug(f"{reply_txt=}")
    logger.debug(f"{update.callback_query=}")
    if update.callback_query:
        keyboard.append([InlineKeyboardButton(text="<< Back", callback_data=RESTART)])
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            text=reply_txt,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML",
            disable_web_page_preview=True,
        )
    else:
        # this pattern is used for simple messages
        keyboard.append([InlineKeyboardButton(text="Exit", callback_data=CANCEL)])
        await update.message.reply_text(
            reply_txt,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML",
            disable_web_page_preview=True,
            disable_notification=settings.DISABLE_NOTIFICATION,
        )

    return EVENT_MENU


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Parses the CallbackQuery and updates the message text."""

    logger.debug(f"{update=}")
    context.user_data["answer"] = update.message.text
    logger.debug(f"{update.message.text=}")
    logger.info(
        f"{update.effective_user.username} (ID={update.effective_user.id}) "
        f'requested "{update.message.text}" in chat ID={update.effective_chat.id}"'
    )
    if re.match(MESSAGE_NEW_EVENT_PATTERNS, update.message.text):
        logger.info("Flushing event context...")
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
        return await get_events_handler(update=update, context=context)
    else:
        await update.message.reply_text(
            f"{update.message.text=}",
            parse_mode="HTML",
            disable_notification=settings.DISABLE_NOTIFICATION,
        )
    return ANSWER


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
        logger.info(
            f"{update.effective_user.username} (ID={update.effective_user.id}) "
            f'selected {date_event} date "{date.strftime("%d.%m.%Y")}"'
        )
        await query.edit_message_text(
            text=f'You selected {date_event} {date.strftime("%d/%m/%Y")}',
        )
        logger.debug("{update=}")
        await edit_event(update, context)
    return END


async def event_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    logger.debug(f"{update.callback_query.data=}")
    logger.debug(f"{context.user_data=}")
    if re.match("^" + str(EVENT_MENU), update.callback_query.data):
        event_id = update.callback_query.data.replace(str(EVENT_MENU), "")
        logger.debug(f'Match "EVENT_MENU" ({EVENT_MENU=})')
    elif re.match("^" + str(BACK), update.callback_query.data):
        logger.debug(f'Match "BACK" ({BACK=})')
        event_id = update.callback_query.data.replace(str(BACK), "")
    logger.info(
        f'User "{update.effective_user.id}" (ID={update.effective_user.id}) '
        f'opened event menu for event "{event_id}" in chat (ID={update.effective_chat.id})'
    )
    events = context.user_data.get("event_list")
    logger.debug(f"{events=}, {event_id=}")
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
    return END


async def edit_event(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    logger.debug(f"{context.user_data=}")
    logger.debug(f"{update.callback_query=}")
    buttons = {
        "summary": "Edit summary",
        "start": "Change start date",
        "end": "Change end date",
        "back": "<< Back",
        "callback": BACK,
        "back_button": InlineKeyboardButton("<< Back", callback_data=str(BACK)),
    }
    if context.user_data.get(NEW_EVENT):
        logger.debug("Before catch exception:")
        buttons["callback"] = RESTART
        # buttons["back"] = "Exit"
        event_dict = context.user_data.get(NEW_EVENT_DICT)
        if not event_dict:
            logger.info("No event dictionary for new event is defined.")
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
        context.user_data["event_list"] = [event]
        buttons["callback"] = BACK + event.id
        logger.debug(f"{context.user_data["event_list"]=}, {event=}")
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
        del keyboard[2][0]
        await update.message.reply_text(
            text=message,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML",
            disable_notification=settings.DISABLE_NOTIFICATION,
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
    logger.info(
        f'Event "{result.get('''summary''')}" {action} by {update.effective_user.username} '
        f"(ID={update.effective_user.id})"
    )
    reply_message = (
        f'Event <a href="'
        f'{result["htmlLink"]}">'
        f"{event_body.summary}</a> "
        f"successfully {action} by "
        f"<b>@{update.effective_user.username}</b>\n"
    )
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            text=reply_message,
            parse_mode="HTML",
            disable_web_page_preview=True,
        )
    else:
        await update.message.reply_text(
            text=reply_message,
            parse_mode="HTML",
            disable_web_page_preview=True,
            disable_notification=settings.DISABLE_NOTIFICATION,
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
    persistent=True if settings.PERSISTENCE else False,
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

conv_handler = ConversationHandler(
    name="main",
    persistent=True if settings.PERSISTENCE else False,
    conversation_timeout=settings.CONVERSATION_TIMEOUT,
    entry_points=[
        CommandHandler("start", start, filters=(Common.chat_acl | Common.admin_acl)),
        MessageHandler(
            (
                filters.Regex(MESSAGE_NEW_EVENT_PATTERNS)
                | filters.Regex(MESSAGE_GET_EVENT_PATTERNS)
            )
            & (Common.chat_acl | Common.admin_acl),
            button,
        ),
    ],
    states={
        ANSWER: [
            CallbackQueryHandler(
                get_events_handler, pattern="^" + str(GET_EVENTS) + "$"
            ),
            CallbackQueryHandler(
                edit_event,
                pattern=("^" + str(EVENT_CREATE) + "$"),
            ),
        ],
        EVENT_EDITOR: [
            CallbackQueryHandler(ask_for_input, pattern="^" + str(EVENT_DESC) + "$"),
            CallbackQueryHandler(save_event, pattern="^" + str(EVENT_SAVE) + "$"),
            CallbackQueryHandler(event_menu_handler, pattern="^" + str(BACK)),
            calendar_select_handler,
        ],
        TYPING: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_input)],
        CANCEL: [CallbackQueryHandler(cancel)],
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
            CallbackQueryHandler(
                edit_event,
                pattern=("^" + str(EDIT_EVENT) + "$"),
            ),
            CallbackQueryHandler(get_events_handler, pattern="^" + str(BACK) + "$"),
        ],
    },
    fallbacks=fallback_handlers
    + [
        CallbackQueryHandler(cancel, pattern="^" + str(CANCEL) + "$"),
        CallbackQueryHandler(start, pattern="^" + str(RESTART) + "$"),
    ],
)
