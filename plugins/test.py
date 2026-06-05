# -------------------------------------------------------------
# CODE POWERED & MAINTAINED BY: YOUR AI ASSISTANT
# Telegram: @Your_Username | Channel: https://t.me/Your_Channel
# -------------------------------------------------------------

import os
import re 
import sys
import asyncio 
import logging 
import time
from database import Db, db
from config import Config, temp
from script import Script
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message 
from pyrogram.errors.exceptions.bad_request_400 import AccessTokenExpired, AccessTokenInvalid
from pyrogram.errors import FloodWait
from typing import Union, Optional, AsyncGenerator
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)

logger = logging.getLogger("AI-Assistant-HelperEngine")
logger.setLevel(logging.INFO)

BTN_URL_REGEX = re.compile(r"(\[([^\[]+?)]\[buttonurl:/{0,2}(.+?)(:same)?])")
BOT_TOKEN_TEXT = (
    "<b>🤖 <u>AI NODE DEPLOYMENT SUITE</u></b>\n\n"
    "1) Head over to the official gateway: @BotFather\n"
    "2) Create a fresh application bot container using <code>/newbot</code>\n"
    "3) Copy or Forward the absolute raw HTTP API Token text message directly to this terminal window."
)
SESSION_STRING_SIZE = 351

class CLIENT: 
    def __init__(self):
        self.api_id = Config.API_ID
        self.api_hash = Config.API_HASH

    def user_session(self, data: str) -> Client:
        return Client("USERBOT", self.api_id, self.api_hash, session_string=data)
         
    async def add_bot(self, bot: Client, message: Message) -> Optional[bool]:
        user_id = int(message.from_user.id)
        msg = await bot.ask(chat_id=user_id, text=BOT_TOKEN_TEXT)
        
        if msg.text == '/cancel':
            return await msg.reply('<b>❌ Session Terminated: Process canceled by user request.</b>')
        elif not msg.forward_date:
            return await msg.reply_text("<b>❌ Verification Error: Provided block is not a valid forwarded Telegram context asset.</b>")
        elif str(msg.forward_from.id) != "93372553":
            return await msg.reply_text("<b>❌ Identity Mismatch: Access token payload must be strictly forwarded from the authentic @BotFather node.</b>")
            
        bot_token_pattern = re.findall(r'\d[0-9]{8,10}:[0-9A-Za-z_-]{35}', msg.text, re.IGNORECASE)
        bot_token = bot_token_pattern[0] if bot_token_pattern else None
        
        if not bot_token:
            return await msg.reply_text("<b>❌ Structural Discrepancy: Encrypted token string format could not be verified in the submitted package.</b>")
            
        loading = await msg.reply_text("🧬 <code>AI Handshaking Node: Attempting synchronization with secure Telegram architecture loops...</code>")
        try:
            _client = Client("BOT", Config.API_ID, Config.API_HASH, bot_token=bot_token, in_memory=True)
            await _client.start()
        except Exception as e:
            await loading.delete()
            await msg.reply_text(f"<b>❌ Node Linkage Fault [BOT COMPONENT EXCEPTION]:</b> `{e}`")
            return
            
        _bot = _client.me
        details = {
            'id': _bot.id,
            'is_bot': True,
            'user_id': user_id,
            'name': _bot.first_name,
            'token': bot_token,
            'username': _bot.username 
        }
        await db.add_bot(details)
        await loading.edit_text("<b>✅ Pipeline Operational: Automation client token synchronized into active cloud clusters!</b>")
        return True

    async def add_session(self, bot: Client, message: Message) -> Optional[bool]:
        user_id = int(message.from_user.id)
        disclaimer_text = (
            "<b>⚠️ <u>CRITICAL COMPLIANCE NOTICE & RISK MATRIX</u> ⚠️</b>\n\n"
            "<code>Integrating a custom user string-session session vector grants the forwarding micro-loops "
            "the capabilities to buffer and sync assets across remote private/restricted workspaces under "
            "your explicit profile node footprint.\n\n"
            "Deploying memory sessions involves risks of profile automation throttling or administrative blocks from Telegram servers. "
            "Our development cluster maintains zero liabilities regarding individual account actions. Proceed at your own risk.</code>"
        )
        await bot.send_message(user_id, text=disclaimer_text)
        await asyncio.sleep(0.5)
        
        phone_number_msg = await bot.ask(chat_id=user_id, text="<b>📱 Provide your active mobile terminal registration identifier (with standard country code prefix):\n\n<u>Example Profile:</u> <code>+13124562345</code></b>")
        if phone_number_msg.text == '/cancel':
            return await phone_number_msg.reply('<b>❌ Process terminated.</b>')
            
        phone_number = phone_number_msg.text.strip().replace(" ", "")
        client = Client(":memory:", Config.API_ID, Config.API_HASH)
        
        await client.connect()
        otp_status_msg = await phone_number_msg.reply("⚡ `AI Communications Core: Dispatching dynamic OTP packet layer to account...`")
        
        try:
            code = await client.send_code(phone_number)
            phone_code_msg = await bot.ask(
                user_id, 
                "<b>📥 OTP Delivery Sync Successful!</b>\n\nCheck your official authentic Telegram system notifications chat for the authentication key code.\n\n"
                "📌 <u>STRICT PROTOCOL SYNTAX REQUIREMENT:</u>\nIf your received code is `54321`, you **MUST** format and transmit it with explicit spaces between values: <code>5 4 3 2 1</code>.\n\n"
                "⌨️ Type <code>/cancel</code> to abort configuration operations.", 
                filters=filters.text, 
                timeout=600
            )
        except PhoneNumberInvalid:
            await otp_status_msg.delete()
            await phone_number_msg.reply('<b>❌ Registration Blocked: Specified phone schema values are unrecognized by Telegram network arrays.</b>')
            return
            
        if phone_code_msg.text == '/cancel':
            return await phone_code_msg.reply('<b>❌ Connection pipeline destroyed by client request.</b>')
            
        try:
            phone_code = phone_code_msg.text.replace(" ", "")
            await client.sign_in(phone_number, code.phone_code_hash, phone_code)
        except PhoneCodeInvalid:
            return await phone_code_msg.reply('<b>❌ Validation Failure: Handshake rejected due to mismatching authentication keys.</b>')
        except PhoneCodeExpired:
            return await phone_code_msg.reply('<b>❌ Verification Timeout: Security window lifecycle expired. Re-trigger registration suite.</b>')
        except SessionPasswordNeeded:
            two_step_msg = await bot.ask(user_id, '<b>🔒 Advanced Layer Triggered: Two-Step Cloud Verification Protection detected. Enter your profile account password token string below:\n\nType /cancel to terminate.</b>', filters=filters.text, timeout=300)
            if two_step_msg.text == '/cancel':
                return await two_step_msg.reply('<b>❌ Authentication procedures dropped.</b>')
            try:
                await client.check_password(password=two_step_msg.text)
            except PasswordHashInvalid:
                return await two_step_msg.reply('<b>❌ Cryptographic Failure: Invalid secondary structural password provided. Access revoked.</b>')
                
        string_session = await client.export_session_string()
        await client.disconnect()
        
        if len(string_session) < SESSION_STRING_SIZE:
            return await phone_code_msg.reply('<b>❌ Integration Failed: Extracted session payload structural sequence is corrupted.</b>')
            
        loading_recovery = await phone_code_msg.reply_text("🧬 `AI Optimization Pipeline: Parsing new account string session footprint vectors...`")
        try:
            _client = Client("USERBOT", self.api_id, self.api_hash, session_string=string_session)
            await _client.start()
        except Exception as e:
            await loading_recovery.delete()
            return await phone_code_msg.reply_text(f"<b>❌ Core Linking Exception [USERBOT RECONSTRUCT FAULT]:</b> `{e}`")
            
        user = _client.me
        details = {
            'id': user.id,
            'is_bot': False,
            'user_id': user_id,
            'name': user.first_name,
            'session': string_session,
            'username': user.username
        }
        await db.add_userbot(details)
        await loading_recovery.edit_text("<b>🎉 Secure Deployment Complete: Your customized userbot connection layer is now active!</b>")
        return True

# -------------------------------------------------------------
# CORE COMMAND EXTENSION MATRICES (AI RESET SYSTEMS)
# -------------------------------------------------------------

@Client.on_message(filters.private & filters.command('reset'))
async def forward_tag(bot, m):
    default = await db.get_configs("01")
    await db.update_configs(m.from_user.id, default)
    await m.reply("<b>✅ Configuration Matrix Flushed: Settings restored back to factory defaults successfully!</b>")

@Client.on_message(filters.command('resetall') & filters.user(Config.BOT_OWNER))
async def resetall(bot, message):
    users = await db.get_all_users()
    status_tracker_msg = await message.reply("⚙️ <code>AI Global Reconfigurer: Allocating transaction loops across cluster arrays...</code>")
    
    TEXT_TEMPLATE = "📊 **Global Clusters Purge Status:**\n• Scanned Logs: `{}`\n• Success Rebuilt: `{}`\n• Write Drops: `{}`\n• Skip Exceptions: `{}`"
    total, success, failed, already = 0, 0, 0, 0
    ERRORS = []
    
    batch_buffer = []
    CONCURRENCY_THRESHOLD = 20

    async def flush_reconfig_batch(batch):
        nonlocal success, failed
        tasks = []
        for user_node in batch:
            u_id = user_node['id']
            # Fetch config node structure
            cfg = await get_configs(u_id)
            cfg['db_uri'] = None
            tasks.append(db.update_configs(u_id, cfg))
            
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for output in results:
            if isinstance(output, Exception):
                ERRORS.append(str(output))
                failed += 1
            else:
                success += 1

    async for user in users:
        total += 1
        batch_buffer.append(user)
        
        if len(batch_buffer) >= CONCURRENCY_THRESHOLD:
            await flush_reconfig_batch(batch_buffer)
            batch_buffer.clear()
            
            if total % 10 == 0:
                try:
                    await status_tracker_msg.edit(TEXT_TEMPLATE.format(total, success, failed, already))
                except Exception:
                    pass
                await asyncio.sleep(0.3)

    if batch_buffer:
        await flush_reconfig_batch(batch_buffer)

    if ERRORS:
        logger.error(f"Global reset array structural drops logged: {ERRORS[:10]}")
        
    await status_tracker_msg.edit(f"<b>✅ Global Operation Complete! All cloud profiles synchronized back to stock schemas.</b>\n\n" + TEXT_TEMPLATE.format(total, success, failed, already))

# -------------------------------------------------------------
# DYNAMIC METADATA ACCESSORS
# -------------------------------------------------------------

async def get_configs(user_id):
    return await db.get_configs(user_id)

async def update_configs(user_id, key, value):
    current = await db.get_configs(user_id)
    if key in ['caption', 'duplicate', 'db_uri', 'forward_tag', 'protect', 'min_size', 'max_size', 'extension', 'keywords', 'button']:
        current[key] = value
    else: 
        current['filters'][key] = value
    await db.update_configs(user_id, current)

async def iter_messages(
    self,
    chat_id: Union[int, str],
    limit: int,
    offset: int = 0,
    filters: dict = None,
    max_size: int = None,
) -> Optional[AsyncGenerator["types.Message", None]]:
    """Hyper-Fast Asynchronous Messaging Iterator Engine."""
    current = offset
    while True:
        new_diff = min(200, limit - current)
        if new_diff <= 0:
            return

        messages = await self.get_messages(chat_id, list(range(current, current + new_diff + 1)))
        for message in messages:
            if filters and any(getattr(message, media_type, False) for media_type in filters):
                yield "FILTERED"
            else:
                yield message
                
            current += 1

async def get_client(bot_token, is_bot=True):
    if is_bot:
        return Client("BOT", Config.API_ID, Config.API_HASH, bot_token=bot_token, in_memory=True)
    return Client("USERBOT", Config.API_ID, Config.API_HASH, session_string=bot_token)

def parse_buttons(text, markup=True):
    buttons = []
    for match in BTN_URL_REGEX.finditer(text):
        n_escapes = 0
        to_check = match.start(1) - 1
        while to_check > 0 and text[to_check] == "\\":
            n_escapes += 1
            to_check -= 1

        if n_escapes % 2 == 0:
            if bool(match.group(4)) and buttons:
                buttons[-1].append(InlineKeyboardButton(
                    text=match.group(2),
                    url=match.group(3).replace(" ", "")))
            else:
                buttons.append([InlineKeyboardButton(
                    text=match.group(2),
                    url=match.group(3).replace(" ", ""))])
                    
    if markup and buttons:
        buttons = InlineKeyboardMarkup(buttons)
    return buttons if buttons else None
