# -------------------------------------------------------------------------
# 🚀 AUTOMATED HYPER-FAST STREAM FORWARDING & ITERATION ENGINE
# 👦 DESIGNED & ARCHITECTURED BY: Ovesh (https://t.me/OveshBoss)
# 📡 CENTRAL UPDATE STREAM: OveshBossOfficial (https://t.me/OveshBossOfficial)
# -------------------------------------------------------------------------

import os
import sys 
import math
import time
import re
import asyncio 
import logging
import random
from .utils import STS
from database import Db, db
from .test import CLIENT, get_client, iter_messages
from config import Config, temp
from script import Script
from pyrogram import Client, filters 
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message 
from .db import connect_user_db

CLIENT = CLIENT()
logger = logging.getLogger("Ovesh-RegixEngine")
TEXT = Script.TEXT

@Client.on_callback_query(filters.regex(r'^start_public'))
async def pub_(bot, message: CallbackQuery):
    user = message.from_user.id
    temp.CANCEL[user] = False
    frwd_id = message.data.split("_")[2]
    
    if temp.lock.get(user) and str(temp.lock.get(user)) == "True":
        return await message.answer("⚠️ System Busy: Please wait until your current ongoing task is completed!", show_alert=True)
        
    sts = STS(frwd_id)
    if not sts.verify():
        await message.answer("⚠️ Expired Session: This transaction button is no longer active.", show_alert=True)
        return await message.message.delete()
        
    i = sts.get(full=True)
    if i.TO in temp.IS_FRWD_CHAT:
        return await message.answer("⚠️ Active Operation Found: A task is already progressing inside the target chat container.", show_alert=True)
        
    m = await msg_edit(message.message, "⚙️ <code>AI Engine: Synchronizing metadata vectors, please hold...</code>")
    _bot, caption, forward_tag, datas, protect, button = await sts.get_data(user)
    
    filter_type = datas['filters']
    max_size = datas['max_size']
    min_size = datas['min_size']
    keyword = datas['keywords']
    exten = datas['extensions']
    
    keywords = "|".join(keyword).rstrip("|") if keyword else None
    extensions = "|".join(exten).rstrip("|") if exten else None
    
    if not _bot:
        return await msg_edit(m, "<code>Configuration Error: No active bot node attached. Please add a bot using /settings !</code>", wait=True)
        
    data = _bot['token'] if _bot['is_bot'] else _bot['session']
    
    try:
        il = True if _bot['is_bot'] else False
        client = await get_client(data, is_bot=il)
        await client.start()
    except Exception as e:  
        logger.error(f"Client handshaking exception: {e}")
        return await m.edit(f"❌ Connection Failed: {e}")
        
    await msg_edit(m, "⚡ <code>AI Engine: Initializing secure network handshake pipeline...</code>")
    
    try: 
        await client.get_messages(sts.get("FROM"), sts.get("limit"))
    except Exception:
        await msg_edit(m, f"❌ **Source Access Denied:** Source chat may be private. Ensure your Userbot is a member or make your [Bot](t.me/{_bot['username']}) an administrator there.", retry_btn(frwd_id), True)
        return await stop(client, user)
        
    try:
        k = await client.send_message(i.TO, "⚡ `AI Pipeline Connection: Active`")
        await k.delete()
    except Exception:
        await msg_edit(m, f"❌ **Target Write Error:** Please ensure your [UserBot / Bot](t.me/{_bot['username']}) has full Admin Permissions inside the Target Channel.", retry_btn(frwd_id), True)
        return await stop(client, user)
        
    user_have_db = False
    dburi = datas['db_uri']
    if dburi is not None:
        connected, user_db = await connect_user_db(user, dburi, i.TO)
        if not connected:
            await msg_edit(m, "⚠️ <code>Database Warning: Direct cluster sync failed. Processing in fallback safe-skipping mode...</code>")
        else:
            user_have_db = True
            
    temp.forwardings += 1
    await db.add_frwd(user)
    await send(client, user, "<b>🚀 Ovesh Engine: Forwarding Pipeline Activated!</b>")
    sts.add(time=True)
    
    sleep_delay = 1 if _bot['is_bot'] else 10
    await msg_edit(m, "📦 <code>AI Engine: Buffering index streams...</code>") 
    temp.IS_FRWD_CHAT.append(i.TO)
    temp.lock[user] = locked = True
    dup_files = []
    
    if locked:
        try:
            MSG = []
            pling = 0
            await edit(user, m, 'PROCESSING', 5, sts)
            
            async for message in iter_messages(client, chat_id=sts.get("FROM"), limit=sts.get("limit"), offset=sts.get("skip"), filters=filter_type, max_size=max_size):
                if await is_cancelled(client, user, m, sts):
                    if user_have_db:
                        await user_db.drop_all()
                        await user_db.close()
                    return
                    
                if pling % 20 == 0: 
                    await edit(user, m, 'PROCESSING', 5, sts)
                pling += 1
                sts.add('fetched')
                
                if message == "DUPLICATE":
                    sts.add('duplicate')
                    continue
                elif message == "FILTERED":
                    sts.add('filtered')
                    continue 
                elif message.empty or message.service:
                    sts.add('deleted')
                    continue
                elif message.document and await extension_filter(extensions, message.document.file_name):
                    sts.add('filtered')
                    continue 
                elif message.document and await keyword_filter(keywords, message.document.file_name):
                    sts.add('filtered')
                    continue 
                elif message.document and await size_filter(max_size, min_size, message.document.file_size):
                    sts.add('filtered')
                    continue 
                elif message.document and message.document.file_id in dup_files:
                    sts.add('duplicate')
                    continue
                    
                if message.document and datas['skip_duplicate']:
                    dup_files.append(message.document.file_id)
                    if user_have_db:
                        await user_db.add_file(message.document.file_id)
                        
                if forward_tag:
                    MSG.append(message.id)
                    notcompleted = len(MSG)
                    completed = sts.get('total') - sts.get('fetched')
                    if notcompleted >= 100 or completed <= 100: 
                        await forward(user, client, MSG, m, sts, protect)
                        sts.add('total_files', notcompleted)
                        await asyncio.sleep(10)
                        MSG = []
                else:
                    new_caption = custom_caption(message, caption)
                    details = {"msg_id": message.id, "media": media(message), "caption": new_caption, 'button': button, "protect": protect}
                    await copy(user, client, details, m, sts)
                    sts.add('total_files')
                    await asyncio.sleep(sleep_delay) 
                    
        except Exception as e:
            logger.error(f"Execution runtime crash: {e}")
            await msg_edit(m, f'<b>⚠️ Operational Error Encountered:</b>\n<code>{e}</code>', wait=True)
            if user_have_db:
                await user_db.drop_all()
                await user_db.close()
            if sts.TO in temp.IS_FRWD_CHAT:
                temp.IS_FRWD_CHAT.remove(sts.TO)
            return await stop(client, user)
            
        if sts.TO in temp.IS_FRWD_CHAT:
            temp.IS_FRWD_CHAT.remove(sts.TO)
            
        await send(client, user, "<b>🎉 System Notice: File stream forwarding finished successfully!</b>")
        await edit(user, m, 'COMPLETED', "completed", sts) 
        if user_have_db:
            await user_db.drop_all()
            await user_db.close()
        await stop(client, user)

async def copy(user, bot, msg, m, sts):
    try:                                       
        if msg.get("media") and msg.get("caption"):
            await bot.send_cached_media(
                chat_id=sts.get('TO'),
                file_id=msg.get("media"),
                caption=msg.get("caption"),
                reply_markup=msg.get('button'),
                protect_content=msg.get("protect")
            )
        else:
            await bot.copy_message(
                chat_id=sts.get('TO'),
                from_chat_id=sts.get('FROM'),    
                caption=msg.get("caption"),
                message_id=msg.get("msg_id"),
                reply_markup=msg.get('button'),
                protect_content=msg.get("protect")
            )
    except FloodWait as e:
        await edit(user, m, 'PROCESSING', e.value, sts)
        await asyncio.sleep(e.value)
        await edit(user, m, 'PROCESSING', 5, sts)
        await copy(user, bot, msg, m, sts)
    except Exception as e:
        logger.debug(f"Copy sequence item deleted/failed: {e}")
        sts.add('deleted')

async def forward(user, bot, msg, m, sts, protect):
    try:                                             
        await bot.forward_messages(
            chat_id=sts.get('TO'),
            from_chat_id=sts.get('FROM'), 
            protect_content=protect,
            message_ids=msg
        )
    except FloodWait as e:
        await edit(user, m, 'PROCESSING', e.value, sts)
        await asyncio.sleep(e.value)
        await edit(user, m, 'PROCESSING', 5, sts)
        await forward(user, bot, msg, m, sts, protect)

async def msg_edit(msg, text, button=None, wait=None):
    try:
        return await msg.edit(text, reply_markup=button)
    except MessageNotModified:
        return msg
    except FloodWait as e:
        if wait:
            await asyncio.sleep(e.value)
            return await msg_edit(msg, text, button, wait)

async def edit(user, msg, title, status, sts):
    i = sts.get(full=True)
    status_text = 'Forwarding' if status == 5 else f"Sleeping {status}s" if str(status).isnumeric() else status
    percentage = "{:.0f}".format(float(i.fetched) * 100 / float(i.total)) if float(i.total) > 0 else "0"
    
    text = TEXT.format(i.fetched, i.total_files, i.duplicate, i.deleted, i.skip, i.filtered, status_text, percentage, title)
    await update_forward(
        user_id=user, last_id=None, start_time=i.start, limit=i.limit, chat_id=i.FROM, toid=i.TO, 
        forward_id=None, msg_id=msg.id, fetched=i.fetched, deleted=i.deleted, total=i.total_files, 
        duplicate=i.duplicate, skip=i.skip, filterd=i.filtered
    )
    
    now = time.time()
    diff = int(now - i.start) if int(now - i.start) > 0 else 1
    speed = sts.divide(i.fetched, diff)
    elapsed_time = round(diff) * 1000
    time_to_completion = round(sts.divide(i.total - i.fetched, int(speed) if int(speed) > 0 else 1)) * 1000
    estimated_total_time = elapsed_time + time_to_completion  
    
    fill_count = min(math.floor(int(percentage) / 4), 24)
    progress = "●" * fill_count + "○" * (24 - fill_count)
    
    button = [
        [InlineKeyboardButton(f"📊 Progress: {percentage}% [{progress}]", f"fwrdstatus#{status_text}#{estimated_total_time}#{percentage}#{i.id}")],
        [
            InlineKeyboardButton('🔄 Refresh Analytics', callback_data=f"fwrdstatus#{status_text}#{estimated_total_time}#{percentage}#{i.id}"),
            InlineKeyboardButton('🛡️ Updates Hub', url='https://t.me/OveshBossOfficial')
        ]
    ]
    
    if status in ["cancelled", "completed"]:
        button.append([InlineKeyboardButton('✨ Pipeline Closed ✨', callback_data="close_btn")])
    else:
        button.append([InlineKeyboardButton('🛑 Abort Stream Transmission', callback_data='terminate_frwd')])
        
    await msg_edit(msg, text, InlineKeyboardMarkup(button))

async def is_cancelled(client, user, msg, sts):
    if temp.CANCEL.get(user) == True:
        if sts.TO in temp.IS_FRWD_CHAT:
            temp.IS_FRWD_CHAT.remove(sts.TO)
        await edit(user, msg, 'CANCELLED', "cancelled", sts)
        await send(client, user, "<b>❌ System Alert: Forwarding transmission aborted by user request.</b>")
        await stop(client, user)
        return True 
    return False 

async def stop(client, user):
    try:
        await client.stop()
    except Exception:
        pass 
    await db.rmve_frwd(user)
    temp.forwardings -= 1
    temp.lock[user] = False 

async def send(bot, user, text):
    try:
        await bot.send_message(user, text=text)
    except Exception:
        pass 

def custom_caption(msg, caption):
    if msg.media:
        if msg.video or msg.document or msg.audio or msg.photo:
            media_obj = getattr(msg, msg.media.value, None)
            if media_obj:
                file_name = getattr(media_obj, 'file_name', '')
                file_size = getattr(media_obj, 'file_size', '')
                fcaption = getattr(msg, 'caption', '')
                if fcaption:
                    fcaption = fcaption.html
                if caption:
                    return caption.format(filename=file_name, size=get_size(file_size), caption=fcaption)
                return fcaption
    return None

def get_size(size):
    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units) - 1:
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i]) 

async def keyword_filter(keywords, file_name):
    if keywords is None:
        return False
    return False if re.search(keywords, file_name, re.IGNORECASE) else True

async def extension_filter(extensions, file_name):
    if extensions is None:
        return False
    return False if re.search(extensions, file_name, re.IGNORECASE) else True

async def size_filter(max_size, min_size, file_size):
    file_size = file_size / 1024 / 1024
    if max_size and min_size == 0:
        return False
    if max_size == 0:
        return file_size < min_size
    if min_size == 0:
        return file_size > max_size
    return False if min_size <= file_size <= max_size else True

def media(msg):
    if msg.media:
        media_obj = getattr(msg, msg.media.value, None)
        if media_obj:
            return getattr(media_obj, 'file_id', None)
    return None 

def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
          ((str(hours) + "h, ") if hours else "") + \
          ((str(minutes) + "m, ") if minutes else "") + \
          ((str(seconds) + "s, ") if seconds else "") + \
          ((str(milliseconds) + "ms, ") if milliseconds else "")
    return tmp[:-2] if tmp else "0s"

def retry_btn(id):
    return InlineKeyboardMarkup([[InlineKeyboardButton('♻️ RE-INITIALIZE CORE PIPELINE ♻️', f"start_public_{id}")]])

@Client.on_callback_query(filters.regex(r'^terminate_frwd$'))
async def terminate_frwding(bot, m: CallbackQuery):
    user_id = m.from_user.id 
    temp.lock[user_id] = False
    temp.CANCEL[user_id] = True 
    await m.answer("💥 Transmission Cancelled Instantly!", show_alert=True)

@Client.on_callback_query(filters.regex(r'^fwrdstatus'))
async def status_msg(bot, msg: CallbackQuery):
    _, status, est_time, percentage, frwd_id = msg.data.split("#")
    sts = STS(frwd_id)
    if not sts.verify():
        fetched, forwarded, remaining = 0, 0, 0
    else:
        fetched, limit, forwarded = sts.get('fetched'), sts.get('limit'), sts.get('total_files')
        remaining = max(limit - fetched, 0)
        
    est_time = TimeFormatter(milliseconds=est_time)
    start_time = sts.get('start')
    uptime = await get_bot_uptime(start_time)
    total = max(sts.get('limit') - sts.get('fetched'), 0)
    time_to_comple = await complete_time(total)
    est_time = est_time if (est_time != '' or status not in ['completed', 'cancelled']) else '0 s'
    
    # Render interactive popup query notice matrix
    PROGRESS_TEMPLATE = "📊 Status: {}%\n• Fetched: {}\n• Forwarded: {}\n• Remaining: {}\n• State: {}\n• ETA: {}\n• Running: {}"
    return await msg.answer(PROGRESS_TEMPLATE.format(percentage, fetched, forwarded, remaining, status, time_to_comple, uptime), show_alert=True)

@Client.on_callback_query(filters.regex(r'^close_btn$'))
async def close(bot, update: CallbackQuery):
    await update.answer()
    await update.message.delete()

@Client.on_message(filters.private & filters.command(['stop']))
async def stop_forward(client, message: Message):
    user_id = message.from_user.id
    sts = await message.reply('⚙️ <code>Aborting current stream operations...</code>')
    await asyncio.sleep(0.5)
    if not await db.is_forwad_exit(message.from_user.id):
        return await sts.edit('❌ **No active transmission channels running currently.**')
    temp.lock[user_id] = False
    temp.CANCEL[user_id] = True
    await sts.edit(f"<b>✅ Safe Lock: System operations intercepted and dropped successfully.</b>", disable_web_page_preview=True)

async def restart_pending_forwads(bot, user):
    user = user['user_id']
    settings = await db.get_forward_details(user)
    try:
        skiping = settings['offset']
        fetch = settings['fetched'] - settings['skip']
        temp.forwardings += 1
        forward_id = await store_vars(user)
        sts = STS(forward_id)
        if settings['chat_id'] is None:
            temp.forwardings -= 1
            return await db.rmve_frwd(user)
        if not sts.verify():
            temp.forwardings -= 1
            return 
        sts.add('fetched', value=fetch)
        sts.add('duplicate', value=settings['duplicate'])
        sts.add('filtered', value=settings['filtered'])
        sts.add('deleted', value=settings['deleted'])
        sts.add('total_files', value=settings['total'])
        m = await bot.get_messages(user, settings['msg_id'])
        _bot, caption, forward_tag, datas, protect, button = await sts.get_data(user)
        i = sts.get(full=True)
        filter_type = datas['filters']
        max_size = datas['max_size']
        min_size = datas['min_size']
        keyword = datas['keywords']
        exten = datas['extensions']
        
        keywords = "|".join(keyword).rstrip("|") if keyword else None
        extensions = "|".join(exten).rstrip("|") if exten else None
        
        if not _bot:
            return await msg_edit(m, "<code>Configuration Error: User configuration missing node pointers.</code>", wait=True)
        data = _bot['token'] if _bot['is_bot'] else _bot['session']
        try:
            il = True if _bot['is_bot'] else False
            client = await get_client(data, is_bot=il)
            await client.start()
        except Exception:  
            return await m.edit("❌ Recoldboot execution handshake failed.")
        try:
            await msg_edit(m, "⚡ <code>Processing container recovery...</code>")
        except Exception:
            return await db.rmve_frwd(user)
        try: 
            await client.get_messages(sts.get("FROM"), sts.get("limit"))
        except Exception:
            await msg_edit(m, f"❌ **Source Access Denied during reload.**", retry_btn(forward_id), True)
            return await stop(client, user)
        try:
            k = await client.send_message(i.TO, "⚡ `Recovery Pipeline Sync: True`")
            await k.delete()
        except Exception:
            await msg_edit(m, f"❌ **Write Access failure during boot recovery.**", retry_btn(forward_id), True)
            return await stop(client, user)
    except Exception:
        return await db.rmve_frwd(user)
        
    user_have_db = False
    dburi = datas['db_uri']
    if dburi is not None:
        connected, user_db = await connect_user_db(user, dburi, i.TO)
        if connected:
            user_have_db = True
            
    try:
        start = settings['start_time']
    except KeyError:
        start = None
    sts.add(time=True, start_time=start)
    sleep_delay = 1 if _bot['is_bot'] else 10
    temp.IS_FRWD_CHAT.append(i.TO)
    temp.lock[user] = locked = True
    dup_files = []
    if user_have_db and datas['skip_duplicate']:
        old_files = await user_db.get_all_files()
        async for ofile in old_files:
            dup_files.append(ofile["file_id"])
            
    if locked:
        try:
            MSG = []
            pling = 0
            await edit(user, m, 'PROCESSING', 5, sts)
            async for message in iter_messages(client, chat_id=sts.get("FROM"), limit=sts.get("limit"), offset=skiping, filters=filter_type, max_size=max_size):
                if await is_cancelled(client, user, m, sts):
                    if user_have_db:
                        await user_db.drop_all()
                        await user_db.close()
                    return
                if pling % 20 == 0: 
                    await edit(user, m, 'PROCESSING', 5, sts)
                pling += 1
                sts.add('fetched')
                if message == "DUPLICATE":
                    sts.add('duplicate')
                    continue
                elif message == "FILTERED":
                    sts.add('filtered')
                    continue 
                elif message.empty or message.service:
                    sts.add('deleted')
                    continue
                elif message.document and await extension_filter(extensions, message.document.file_name):
                    sts.add('filtered')
                    continue 
                elif message.document and await keyword_filter(keywords, message.document.file_name):
                    sts.add('filtered')
                    continue 
                elif message.document and await size_filter(max_size, min_size, message.document.file_size):
                    sts.add('filtered')
                    continue 
                elif message.document and message.document.file_id in dup_files:
                    sts.add('duplicate')
                    continue
                if message.document and datas['skip_duplicate']:
                    dup_files.append(message.document.file_id)
                    if user_have_db:
                        await user_db.add_file(message.document.file_id)
                if forward_tag:
                    MSG.append(message.id)
                    notcompleted = len(MSG)
                    completed = sts.get('total') - sts.get('fetched')
                    if notcompleted >= 100 or completed <= 100: 
                        await forward(user, client, MSG, m, sts, protect)
                        sts.add('total_files', notcompleted)
                        await asyncio.sleep(10)
                        MSG = []
                else:
                    new_caption = custom_caption(message, caption)
                    details = {"msg_id": message.id, "media": media(message), "caption": new_caption, 'button': button, "protect": protect}
                    await copy(user, client, details, m, sts)
                    sts.add('total_files')
                    await asyncio.sleep(sleep_delay) 
        except Exception as e:
            await msg_edit(m, f'<b>⚠️ Operational Error:</b>\n<code>{e}</code>', wait=True)
            if user_have_db:
                await user_db.drop_all()
                await user_db.close()
            if sts.TO in temp.IS_FRWD_CHAT:
                temp.IS_FRWD_CHAT.remove(sts.TO)
            return await stop(client, user)
            
        if sts.TO in temp.IS_FRWD_CHAT:
            temp.IS_FRWD_CHAT.remove(sts.TO)
        await send(client, user, "<b>🎉 Coldboot Transmission Complete.</b>")
        if user_have_db:
            await user_db.drop_all()
            await user_db.close()
        await edit(user, m, 'COMPLETED', "completed", sts) 
        await stop(client, user)

async def store_vars(user_id):
    settings = await db.get_forward_details(user_id)
    fetch = settings['fetched']
    forward_id = f'{user_id}-{fetch}'
    STS(id=forward_id).store(settings['chat_id'], settings['toid'], settings['skip'], settings['limit'])
    return forward_id

async def restart_forwards(client):
    users = await db.get_all_frwd()
    tasks = []
    async for user in users:
        tasks.append(restart_pending_forwads(client, user))
    await asyncio.gather(*tasks)

async def update_forward(user_id, chat_id, start_time, toid, last_id, limit, forward_id, msg_id, fetched, total, duplicate, deleted, skip, filterd):
    details = {
        'chat_id': chat_id, 'toid': toid, 'forward_id': forward_id, 'last_id': last_id,
        'limit': limit, 'msg_id': msg_id, 'start_time': start_time, 'fetched': fetched,
        'offset': fetched, 'deleted': deleted, 'total': total, 'duplicate': duplicate,
        'skip': skip, 'filtered': filterd
    }
    await db.update_forward(user_id, details)

async def get_bot_uptime(start_time):
    uptime_seconds = int(time.time() - start_time)
    uptime_minutes = uptime_seconds // 60
    uptime_hours = uptime_minutes // 60
    uptime_days = uptime_hours // 24
    uptime_weeks = uptime_days // 7
    
    uptime_string = ""
    if uptime_weeks != 0: uptime_string += f"{uptime_weeks % 7}w, "
    if uptime_days != 0: uptime_string += f"{uptime_days % 24}d, "
    if uptime_hours != 0: uptime_string += f"{uptime_hours % 24}h, "
    if uptime_minutes != 0: uptime_string += f"{uptime_minutes % 60}m, "
    uptime_string += f"{uptime_seconds % 60}s"
    return uptime_string  

async def complete_time(total_files, files_per_minute=30):
    minutes_required = total_files / files_per_minute
    seconds_required = minutes_required * 60
    weeks = seconds_required // (7 * 24 * 60 * 60)
    days = (seconds_required % (7 * 24 * 60 * 60)) // (24 * 60 * 60)
    hours = (seconds_required % (24 * 60 * 60)) // (60 * 60)
    minutes = (seconds_required % (60 * 60)) // 60
    seconds = seconds_required % 60
    
    time_format = ""
    if weeks > 0: time_format += f"{int(weeks)}w, "
    if days > 0: time_format += f"{int(days)}d, "
    if hours > 0: time_format += f"{int(hours)}h, "
    if minutes > 0: time_format += f"{int(minutes)}m, "
    if seconds > 0: time_format += f"{int(seconds)}s"
    return time_format.rstrip(", ") if time_format else "0s"
