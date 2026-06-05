# -------------------------------------------------------------------------
# 📡 ADVANCED PUBLIC FILE-FORWARDING PIPELINE ENGINE
# 👦 DESIGNED & ARCHITECTURED BY: Ovesh (https://t.me/OveshBoss)
# 📡 CENTRAL UPDATE STREAM: OveshBossOfficial (https://t.me/OveshBossOfficial)
# -------------------------------------------------------------------------

import re
import asyncio 
import logging
from .utils import STS
from database import Db, db
from config import temp 
from script import Script
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait 
from pyrogram.errors.exceptions.not_acceptable_406 import ChannelPrivate as PrivateChat
from pyrogram.errors.exceptions.bad_request_400 import ChannelInvalid, ChatAdminRequired, UsernameInvalid, UsernameNotModified, ChannelPrivate
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

logger = logging.getLogger("Ovesh-PublicEngine")

@Client.on_message(filters.private & filters.command(["forward"]))
async def run(bot, message):
    buttons = []
    btn_data = {}
    user_id = message.from_user.id
    
    # Authenticating linked auxiliary robot nodes
    _bot = await db.get_bot(user_id)
    if not _bot:
        _bot = await db.get_userbot(user_id)
        if not _bot:
            return await message.reply("<code>You haven't added any bot yet. Please configure a bot node via /settings first!</code>")
            
    channels = await db.get_user_channels(user_id)
    if not channels:
        return await message.reply_text("⚠️ Please configure your target channel destination in /settings before initiating a forward operation.")
        
    if len(channels) > 1:
        for channel in channels:
            buttons.append([KeyboardButton(f"{channel['title']}")])
            btn_data[channel['title']] = channel['chat_id']
        buttons.append([KeyboardButton("Cancel")]) 
        
        _toid = await bot.ask(
            message.chat.id, 
            Script.TO_MSG.format(_bot['name'], _bot['username']), 
            reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True)
        )
        if _toid.text.lower().startswith(('/', 'cancel')):
            return await message.reply_text(Script.CANCEL, reply_markup=ReplyKeyboardRemove())
            
        to_title = _toid.text
        toid = btn_data.get(to_title)
        if not toid:
            return await message.reply_text("❌ Selection Error: Unauthorized or invalid channel chosen.", reply_markup=ReplyKeyboardRemove())
    else:
        toid = channels[0]['chat_id']
        to_title = channels[0]['title']
        
    fromid = await bot.ask(message.chat.id, Script.FROM_MSG, reply_markup=ReplyKeyboardRemove())
    if fromid.text and fromid.text.startswith('/'):
        await message.reply(Script.CANCEL)
        return 
        
    if fromid.text and not fromid.forward_date:
        regex = re.compile(r"(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$")
        match = regex.match(fromid.text.replace("?single", ""))
        if not match:
            return await message.reply('❌ Invalid Link Pattern: Please provide a valid Telegram message or channel link.')
            
        chat_id = match.group(4)
        last_msg_id = int(match.group(5))
        if chat_id.isnumeric():
            chat_id = int(("-100" + chat_id))
    elif fromid.forward_from_chat and fromid.forward_from_chat.type in [enums.ChatType.CHANNEL, enums.ChatType.SUPERGROUP]:
        last_msg_id = fromid.forward_from_message_id
        chat_id = fromid.forward_from_chat.username or fromid.forward_from_chat.id
        if last_msg_id is None:
            return await message.reply_text("⚠️ **Notice:** This seems to be a message from a group forwarded by an anonymous admin. Please copy and send the specific text/link instead.")
    else:
        await message.reply_text("❌ **Invalid Source Context:** Provided data source cannot be analyzed.")
        return 
        
    try:
        title = (await bot.get_chat(chat_id)).title
    except (PrivateChat, ChannelPrivate, ChannelInvalid):
        title = "Private Space" if fromid.text else fromid.forward_from_chat.title
    except (UsernameInvalid, UsernameNotModified):
        return await message.reply('❌ Exception: Target link structural integrity verification failed.')
    except Exception as e:
        logger.error(f"Error resolving chat details: {e}")
        return await message.reply(f'⚠️ Pipeline System Error: {e}')
        
    skipno = await bot.ask(message.chat.id, Script.SKIP_MSG)
    if skipno.text.startswith('/'):
        await message.reply(Script.CANCEL)
        return
        
    forward_id = f"{user_id}-{skipno.id}"
    confirmation_buttons = [[
        InlineKeyboardButton('✅ Confirm & Start', callback_data=f"start_public_{forward_id}"),
        InlineKeyboardButton('❌ Abort Process', callback_data="close_btn")
    ]]
    
    reply_markup = InlineKeyboardMarkup(confirmation_buttons)
    await message.reply_text(
        text=Script.DOUBLE_CHECK.format(botname=_bot['name'], botuname=_bot['username'], from_chat=title, to_chat=to_title, skip=skipno.text),
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )
    STS(forward_id).store(chat_id, toid, int(skipno.text), int(last_msg_id))
