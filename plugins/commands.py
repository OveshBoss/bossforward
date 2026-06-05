# -------------------------------------------------------------------------
# 🤖 AI-ENGINE COMMAND HUB & LIVE PERMISSION VALIDATOR PROTOCOL
# 👦 DESIGNED & ARCHITECTURED BY: Ovesh (https://t.me/OveshBoss)
# 📡 CENTRAL UPDATE STREAM: OveshBossOfficial (https://t.me/OveshBossOfficial)
# -------------------------------------------------------------------------

import os
import sys
import asyncio 
import psutil
import time
import logging
from database import db
from config import Config, temp
from script import Script
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import UserNotParticipant

START_TIME = time.time()
logger = logging.getLogger("Ovesh-CommandEngine")

# -------------------------------------------------------------------------
# 🖼️ WELCOME IMAGE SETUP (AMK - INSERT YOUR LINK HERE BHAI)
# -------------------------------------------------------------------------
# Is double quotes "" ke andar apni direct image link paste kar dena bhai.
WELCOME_PIC_URL = "" 

# Main persistent buttons configuration menu
main_buttons = [
    [
        InlineKeyboardButton('❣️ ᴅᴇᴠᴇʟᴏᴘᴇʀ ❣️', url='https://t.me/Ovesh_Boss')
    ],
    [
        InlineKeyboardButton('🔍 sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ', url='https://t.me/OnlyBossMoviesGroup'),
        InlineKeyboardButton('🤖 ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ', url='https://t.me/OveshBossOfficial')
    ],
    [
        InlineKeyboardButton('💝 sᴜʙsᴄʀɪʙᴇ ᴍʏ ʏᴏᴜᴛᴜʙᴇ ᴄʜᴀɴɴᴇʟ', url='https://youtube.com/@OveshBoss')
    ],
    [
        InlineKeyboardButton('👨‍💻 ʜᴇʟᴘ', callback_data='help'),
        InlineKeyboardButton('💁 ᴀʙᴏᴜᴛ', callback_data='about')
    ],
    [
        InlineKeyboardButton('⚙ sᴇᴛᴛɪɴɢs', callback_data='settings#main')
    ]
]

async def check_force_join(client: Client, user_id: int) -> bool:
    """Core runtime validation routine to check channel authorization state."""
    try:
        # Targets the primary brand channel node @OveshBossOfficial
        member = await client.get_chat_member("OveshBossOfficial", user_id)
        if member.status in ["kicked", "left"]:
            return False
        return True
    except UserNotParticipant:
        return False
    except Exception as e:
        logger.error(f"Error checking force join: {e}")
        return True # Fallback to prevent bot lockout in case of api restrictions

def get_force_join_markup() -> InlineKeyboardMarkup:
    """Generates the subscription anchor interface dynamically."""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📢 Join Updates Channel", url="https://t.me/OveshBossOfficial")
        ],
        [
            InlineKeyboardButton("🔄 Try Again / Verified", callback_data="check_verification")
        ]
    ])

# -------------------------------------------------------------------------
# 📡 INTERACTIVE MESSAGE HANDLERS (START & RESTART COMMAND BUFFERS)
# -------------------------------------------------------------------------

@Client.on_message(filters.private & filters.command(['start']))
async def start(client, message):
    user = message.from_user
    
    # Save user context if not tracked in cluster index
    if not await db.is_user_exist(user.id):
        await db.add_user(user.id, user.first_name)
        
    # Phase 1: Initialize interactive AI Processing Status layout
    processing_msg = await message.reply_text("🔍 `AI Engine: Analyzing secure database clusters...`")
    await asyncio.sleep(0.6)
    await processing_msg.edit_text("🛡️ `AI Engine: Verifying security membership token vectors...`")
    await asyncio.sleep(0.5)
    
    # Phase 2: Structural Verification Checks
    is_joined = await check_force_join(client, user.id)
    
    if not is_joined:
        await processing_msg.delete()
        explain_text = (
            f"⚡ **Access Denied | Verification Required**\n\n"
            f"Hello {user.first_name}, our automated core protection engine has detected that "
            f"you have not joined our official updates hub yet.\n\n"
            f"To access this hyper-fast advanced forwarding suite, please click the button below "
            f"to join our channel, then hit the verification refresh trigger button to unlock your workspace node!"
        )
        await message.reply_text(
            text=explain_text,
            reply_markup=get_force_join_markup()
        )
        return

    # Phase 3: Successful Validation - Grant access payload
    await processing_msg.edit_text("⚡ `AI Engine: Authorization Granted! Allocating processing memory threads...`")
    await asyncio.sleep(0.4)
    await processing_msg.delete()
    
    welcome_text = Script.START_TXT.format(user.first_name)
    reply_markup = InlineKeyboardMarkup(main_buttons)
    
    if WELCOME_PIC_URL:
        try:
            await message.reply_photo(
                photo=WELCOME_PIC_URL,
                caption=welcome_text,
                reply_markup=reply_markup
            )
            return
        except Exception as e:
            logger.error(f"Failed sending photo fallback to text: {e}")
            
    await message.reply_text(text=welcome_text, reply_markup=reply_markup)


@Client.on_message(filters.private & filters.command(['restart']) & filters.user(Config.BOT_OWNER))
async def restart(client, message):
    msg = await message.reply_text(text="<i>⚡ AI Engine Initializing System Cold-Boot Procedures...</i>")
    await asyncio.sleep(3)
    await msg.edit("<i>✅ Core pipelines synchronized. Git syncing active repository assets...</i>")
    os.system("git pull -f && pip3 install --no-cache-dir -r requirements.txt")
    os.execle(sys.executable, sys.executable, "main.py", os.environ)

# -------------------------------------------------------------------------
# 🎛️ CALLBACK ROUTINES INTERFACE MANAGEMENT HUB
# -------------------------------------------------------------------------

@Client.on_callback_query(filters.regex(r'^check_verification'))
async def verify_user_callback(client: Client, query: CallbackQuery):
    """Refreshes status tracking instantly upon user explicit validation request."""
    user_id = query.from_user.id
    
    # Flash status parsing banner
    await query.message.edit_text("🔄 `AI Verification Core: Recalculating access tokens...`")
    await asyncio.sleep(0.8)
    
    is_joined = await check_force_join(client, user_id)
    
    if not is_joined:
        await query.answer("❌ Authentication failed! You must join the channel first.", show_alert=True)
        explain_text = (
            f"⚠️ **Access Still Restricted!**\n\n"
            f"Dear {query.from_user.first_name}, the pipeline database could not find your subscription "
            f"inside @OveshBossOfficial.\n\n"
            f"Please make sure you have actively clicked 'Join' and try verifying your status again."
        )
        await query.message.edit_text(text=explain_text, reply_markup=get_force_join_markup())
        return
        
    await query.answer("🎉 Verification successful! Welcome back.", show_alert=True)
    welcome_text = Script.START_TXT.format(query.from_user.first_name)
    reply_markup = InlineKeyboardMarkup(main_buttons)
    
    # If photo verification exists update content space smoothly
    if WELCOME_PIC_URL:
        try:
            await query.message.delete()
            await client.send_photo(
                chat_id=user_id,
                photo=WELCOME_PIC_URL,
                caption=welcome_text,
                reply_markup=reply_markup
            )
            return
        except Exception:
            pass
            
    await query.message.edit_text(text=welcome_text, reply_markup=reply_markup)


@Client.on_callback_query(filters.regex(r'^help'))
async def helpcb(bot, query: CallbackQuery):
    buttons = [
        [InlineKeyboardButton('🤔 ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴍᴇ ❓', callback_data='how_to_use')],
        [InlineKeyboardButton('Aʙᴏᴜᴛ ✨️', callback_data='about'), InlineKeyboardButton('⚙ Sᴇᴛᴛɪɴɢs', callback_data='settings#main')],
        [InlineKeyboardButton('• back', callback_data='back')]
    ]
    await query.message.edit_text(text=Script.HELP_TXT, reply_markup=InlineKeyboardMarkup(buttons))


@Client.on_callback_query(filters.regex(r'^how_to_use'))
async def how_to_use(bot, query: CallbackQuery):
    buttons = [[InlineKeyboardButton('• back', callback_data='help')]]
    await query.message.edit_text(text=Script.HOW_USE_TXT, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)


@Client.on_callback_query(filters.regex(r'^back'))
async def back(bot, query: CallbackQuery):
    await query.message.edit_text(text=Script.START_TXT.format(query.from_user.first_name), reply_markup=InlineKeyboardMarkup(main_buttons))


@Client.on_callback_query(filters.regex(r'^about'))
async def about(bot, query: CallbackQuery):
    buttons = [[InlineKeyboardButton('• back', callback_data='help'), InlineKeyboardButton('Stats ✨️', callback_data='status')]]
    await query.message.edit_text(text=Script.ABOUT_TXT, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)


@Client.on_callback_query(filters.regex(r'^status'))
async def status(bot, query: CallbackQuery):
    users_count, bots_count = await db.total_users_bots_count()
    forwardings = await db.forwad_count()
    upt = await get_bot_uptime(START_TIME)
    buttons = [[InlineKeyboardButton('• back', callback_data='help'), InlineKeyboardButton('System Stats ✨️', callback_data='systm_sts')]]
    await query.message.edit_text(text=Script.STATUS_TXT.format(upt, users_count, bots_count, forwardings), reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)


@Client.on_callback_query(filters.regex(r'^systm_sts'))
async def sys_status(bot, query: CallbackQuery):
    buttons = [[InlineKeyboardButton('• back', callback_data='help')]]
    ram = psutil.virtual_memory().percent
    cpu = psutil.cpu_percent()
    disk_usage = psutil.disk_usage('/')
    total_space = disk_usage.total / (1024**3)
    used_space = disk_usage.used / (1024**3)
    free_space = disk_usage.free / (1024**3)
    
    text = f"""
╔════❰ sᴇʀᴠᴇʀ sᴛᴀᴛs ❱═❍⊱❁۪۪
║╭━━━━━━━━━━━━━━━➣
║┣⪼ <b>ᴛᴏᴛᴀʟ ᴅɪsᴋ sᴘᴀᴄᴇ</b>: <code>{total_space:.2f} GB</code>
║┣⪼ <b>ᴜsᴇᴅ</b>: <code>{used_space:.2f} GB</code>
║┣⪼ <b>ꜰʀᴇᴇ</b>: <code>{free_space:.2f} GB</code>
║┣⪼ <b><b>ᴄᴘᴜ ʟᴏᴀᴅ</b></b>: <code>{cpu}%</code>
║┣⪼ <b><b>ʀᴀᴍ ᴜᴛɪʟɪᴢᴀᴛɪᴏɴ</b></b>: <code>{ram}%</code>
║╰━━━━━━━━━━━━━━━➣
╚══════════════════❍⊱❁۪۪
"""
    await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)


async def get_bot_uptime(start_time):
    uptime_seconds = int(time.time() - start_time)
    uptime_minutes = uptime_seconds // 60
    uptime_hours = uptime_minutes // 60
    uptime_days = uptime_hours // 24
    
    uptime_string = ""
    if uptime_days > 0:
        uptime_string += f"{uptime_days}D "
    if uptime_hours != 0:
        uptime_string += f"{uptime_hours % 24}H "
    if uptime_minutes != 0:
        uptime_string += f"{uptime_minutes % 60}M "
    uptime_string += f"{uptime_seconds % 60}S"
    return uptime_string
