# -------------------------------------------------------------
# CODE POWERED & MAINTAINED BY: ovesh
# -------------------------------------------------------------

import re
import asyncio
import base64
import struct
import logging
from database import Db, db
from config import temp
from .test import CLIENT, get_client
from script import Script
from pyrogram.file_id import FileId
from pyrogram import Client, filters, enums 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

CLIENT = CLIENT()
logger = logging.getLogger("AI-Assistant-UnequifyEngine")

# Dynamic customized completion and verification layers
COMPLETED_BTN = InlineKeyboardMarkup([
    [InlineKeyboardButton('🛡️ Official Updates Hub', url='https://t.me/Your_Channel')],
    [InlineKeyboardButton('✨ Close Workspace ✨', callback_data='close_btn')]
])
CANCEL_BTN = InlineKeyboardMarkup([[InlineKeyboardButton('🛑 Abort Stream Task', 'terminate_frwd')]])

def encode_file_id(s: bytes) -> str:
    """Encodes raw structured database byte blocks into standardized string components."""
    r = b""
    n = 0
    for i in s + bytes([22]) + bytes([4]):
        if i == 0:
            n += 1
        else:
            if n:
                r += b"\x00" + bytes([n])
                n = 0
            r += bytes([i])
    return base64.urlsafe_b64encode(r).decode().rstrip("=")

def unpack_new_file_id(new_file_id: str) -> str:
    """Decodes modern Telegram file unique IDs to extract structural media footprint references."""
    decoded = FileId.decode(new_file_id)
    return encode_file_id(
        struct.pack(
            "<iiqq",
            int(decoded.file_type),
            decoded.dc_id,
            decoded.media_id,
            decoded.access_hash
        )
    )

@Client.on_message(filters.command("unequify") & filters.private)
async def unequify(client: Client, message):
    user_id = message.from_user.id
    temp.CANCEL[user_id] = False
    
    if temp.lock.get(user_id) and str(temp.lock.get(user_id)) == "True":
        return await message.reply("⚠️ **System Busy:** Please wait until your active ongoing task cycle finishes execution.")
        
    _bot = await db.get_userbot(user_id)
    if not _bot:
        return await message.reply("<b>❌ Error: This protocol requires a Userbot configuration node. Please link a Userbot account via /settings</b>")
        
    target = await client.ask(user_id, text="<b>🎯 <u>DUPLICATE SCANNER HUB</u></b>\n\nForward the last text message from your target chat or submit the last specific message URL link below:\n\n⌨️ Send /cancel to terminate session.")
    if target.text and target.text.startswith("/"):
        return await message.reply("<b>❌ Operation aborted by user.</b>")
        
    if target.text:
        regex = re.compile(r"(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$")
        match = regex.match(target.text.replace("?single", ""))
        if not match:
            return await message.reply('<b>❌ Link Parsing Error: Provided URL formatting mismatch.</b>')
        chat_id = match.group(4)
        if chat_id.isnumeric():
            chat_id = int(("-100" + chat_id))
    elif target.forward_from_chat and target.forward_from_chat.type in [enums.ChatType.CHANNEL, enums.ChatType.SUPERGROUP]:
        chat_id = target.forward_from_chat.username or target.forward_from_chat.id
    else:
        return await message.reply_text("<b>❌ Access Refused: Source context type could not be validated.</b>")
        
    confirm = await client.ask(user_id, text="<b>⚠️ <u>CONFIRM MATRIX PURGE</u></b>\n\nAre you sure you want to initialize the deep cleanup sweep?\n\n🔹 Type <code>/yes</code> to run the engine.\n🔹 Type <code>/no</code> to abort.")
    if confirm.text.lower() != '/yes':
        return await confirm.reply("<b>❌ Scan Sequence canceled.</b>")
        
    status_msg = await confirm.reply("⚡ `AI Engine: Deploying dedicated cleaning socket instances...`")
    data = _bot['session']
    
    try:
        bot_client = await get_client(data, is_bot=False)
        await bot_client.start()
    except Exception as e:
        logger.error(f"Failed starting clean socket node: {e}")
        return await status_msg.edit(f"<b>❌ Execution Socket Crash:</b> `{e}`")
        
    try:
        k = await bot_client.send_message(chat_id, text="⚡ `AI Cleanup Loop Validation: Success`")
        await k.delete()
    except Exception:
        await status_msg.edit(f"<b>❌ Write Verification Blocked: Please ensure userbot is an admin in target chat container with Delete Messages permissions.</b>")
        return await bot_client.stop()
        
    # Supercharged using Hash-Set matching algorithms [O(1) Speed Optimization]
    MESSAGES_SET = set()
    DUPLICATE_QUEUE = []
    total_scanned = 0
    total_deleted = 0
    
    temp.lock[user_id] = True
    temp.CANCEL[user_id] = False
    
    try:
        await status_msg.edit(Script.DUPLICATE_TEXT.format(total_scanned, total_deleted, "PROCESSING"), reply_markup=CANCEL_BTN)
        
        # Iterating selectively across raw document objects
        async for msg in bot_client.search_messages(chat_id=chat_id, filter=enums.MessagesFilter.DOCUMENT):
            if temp.CANCEL.get(user_id) == True:
                await status_msg.edit(Script.DUPLICATE_TEXT.format(total_scanned, total_deleted, "CANCELLED"), reply_markup=COMPLETED_BTN)
                return await bot_client.stop()
                
            if not msg.document:
                continue
                
            file_footprint = unpack_new_file_id(msg.document.file_id) 
            
            if file_footprint in MESSAGES_SET:
                DUPLICATE_QUEUE.append(msg.id)
            else:
                MESSAGES_SET.add(file_footprint)
                
            total_scanned += 1
            
            if total_scanned % 500 == 0:
                await status_msg.edit(Script.DUPLICATE_TEXT.format(total_scanned, total_deleted, "PROCESSING"), reply_markup=CANCEL_BTN)
                
            if len(DUPLICATE_QUEUE) >= 100:
                await bot_client.delete_messages(chat_id, DUPLICATE_QUEUE)
                total_deleted += len(DUPLICATE_QUEUE)
                await status_msg.edit(Script.DUPLICATE_TEXT.format(total_scanned, total_deleted, "PROCESSING"), reply_markup=CANCEL_BTN)
                DUPLICATE_QUEUE.clear()
                await asyncio.sleep(0.5) # Adaptive pacing throttling to prevent peer API limits flood
                
        if DUPLICATE_QUEUE:
            await bot_client.delete_messages(chat_id, DUPLICATE_QUEUE)
            total_deleted += len(DUPLICATE_QUEUE)
            
    except Exception as runtime_error:
        temp.lock[user_id] = False 
        logger.error(f"Unequify processing exception: {runtime_error}")
        await status_msg.edit(f"<b>⚠️ Operation Terminated: Internal runtime exception caught.</b>\n\n`{runtime_error}`")
        return await bot_client.stop()
        
    temp.lock[user_id] = False
    await status_msg.edit(Script.DUPLICATE_TEXT.format(total_scanned, total_deleted, "COMPLETED"), reply_markup=COMPLETED_BTN)
    await bot_client.stop()
