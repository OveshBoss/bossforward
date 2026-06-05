# -------------------------------------------------------------------------
# 🤖 AI-ENGINE RECONSTRUCTION - HYPER-FAST MULTI-THREADED BROADCAST SYSTEM
# 👦 ENGINEERED & OPTIMIZED BY: Ovesh (https://t.me/Ovesh_Boss)
# 📡 NETWORKING UPDATE NODE: OveshBossOfficial (https://t.me/OveshBossOfficial)
# -------------------------------------------------------------------------

import time
import asyncio
import logging
import datetime
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import InputUserDeactivated, UserNotParticipant, FloodWait, UserIsBlocked, PeerIdInvalid
from database import db
from config import Config, temp

logger = logging.getLogger("Ovesh-Broadcast Engine")
logger.setLevel(logging.INFO)

# Global status tracking matrix for multi-threaded operations
BROADCAST_STATUS = {}

async def execute_delivery(user_id: int, message, send_as_forward: bool) -> str:
    """Core optimization delivery engine running on parallel tasks."""
    try:
        if send_as_forward:
            await message.forward(chat_id=user_id)
        else:
            await message.copy(chat_id=user_id)
        return "success"
    except FloodWait as e:
        # Smart adaptive backoff routine
        await asyncio.sleep(e.value)
        return await execute_delivery(user_id, message, send_as_forward)
    except InputUserDeactivated:
        await db.delete_user(user_id)
        return "deleted"
    except UserIsBlocked:
        return "blocked"
    except PeerIdInvalid:
        await db.delete_user(user_id)
        return "invalid"
    except Exception:
        return "failed"

@Client.on_message(filters.command("broadcast") & filters.user(Config.BOT_OWNER) & filters.reply)
async def ovesh_core_broadcast(bot: Client, message):
    b_msg = message.reply_to_message
    cmd_args = message.text.split()
    
    # Check if forward flag (-f) is injected into the command parameters
    send_as_forward = "-f" in cmd_args

    broadcast_id = int(time.time())
    BROADCAST_STATUS[broadcast_id] = {"run": True}

    status_msg = await message.reply_text(
        text="⚡ `AI Engine initializing mass broadcast pipelines...`",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("❌ Cancel Broadcast", callback_data=f"stop_brd_{broadcast_id}")
        ]])
    )

    start_time = time.time()
    total_users = await db.total_users_count()
    
    success, blocked, deleted, failed, done = 0, 0, 0, 0, 0
    user_buffer = []
    
    # High-Performance Concurrency Batch Chunk limit
    CONCURRENCY_LIMIT = 25 

    async def flush_batch(batch):
        nonlocal success, blocked, deleted, failed, done
        tasks = [execute_delivery(int(user['id']), b_msg, send_as_forward) for user in batch if 'id' in user]
        results = await asyncio.gather(*tasks)
        
        for res in results:
            done += 1
            if res == "success": success += 1
            elif res == "blocked": blocked += 1
            elif res == "deleted": deleted += 1
            else: failed += 1

    users_cursor = await db.get_all_users()

    async for user in users_cursor:
        # Check if cancellation anchor was triggered via callback interface
        if not BROADCAST_STATUS.get(broadcast_id, {}).get("run", True):
            break
            
        user_buffer.append(user)
        
        if len(user_buffer) >= CONCURRENCY_LIMIT:
            await flush_batch(user_buffer)
            user_buffer.clear()
            
            # Live ETA & Performance Speed Analytics Matrix Calculation
            elapsed_time = time.time() - start_time
            speed = done / elapsed_time if elapsed_time > 0 else 0
            remaining_users = total_users - done
            eta_seconds = int(remaining_users / speed) if speed > 0 else 0
            eta = str(datetime.timedelta(seconds=eta_seconds))

            try:
                await status_msg.edit_text(
                    text=(
                        f"🧬 **Ovesh AI Broadcast In Progress**\n"
                        f"====================================\n"
                        f"📊 **Progress:** `{done}/{total_users}`\n"
                        f"✅ **Success:** `{success}`\n"
                        f"🚫 **Blocked:** `{blocked}`\n"
                        f"💀 **Deleted Accounts:** `{deleted}`\n"
                        f"❌ **Failed Pipes:** `{failed}`\n\n"
                        f"⚡ **Speed:** `{speed:.2f} msgs/sec`\n"
                        f"⏳ **ETA Countdown:** `{eta}`\n"
                        f"====================================\n"
                        f"📡 *Mode: {'Forwarding' if send_as_forward else 'Clean Copying'}*"
                    ),
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton("❌ Cancel Broadcast", callback_data=f"stop_brd_{broadcast_id}")
                    ]])
                )
            except Exception:
                pass
            
            # Anti-flood optimization threshold delay sleep
            await asyncio.sleep(0.5)

    # Process left-over queue stack buffer items
    if user_buffer and BROADCAST_STATUS.get(broadcast_id, {}).get("run", True):
        await flush_batch(user_buffer)

    time_taken = str(datetime.timedelta(seconds=int(time.time() - start_time)))
    is_cancelled = not BROADCAST_STATUS.get(broadcast_id, {}).get("run", True)
    
    final_status = "⚠️ Broadcast Aborted Manually!" if is_cancelled else "✅ Broadcast Processing Completed!"

    await status_msg.edit_text(
        text=(
            f"🔮 **{final_status}**\n"
            f"====================================\n"
            f"⏱️ **Time Elapsed:** `{time_taken}`\n"
            f"👥 **Total Registered Users:** `{total_users}`\n"
            f"📦 **Processed Deliveries:** `{done}`\n"
            f"🎉 **Successfully Delivered:** `{success}`\n"
            f"🚫 **Users Blocked Bot:** `{blocked}`\n"
            f"💀 **Accounts Cleaned:** `{deleted}`\n"
            f"❌ **Total System Drops:** `{failed}`\n"
            f"====================================\n"
            f"👑 Modded Engine Node: [Ovesh](https://t.me/OveshBoss)"
        )
    )
    
    # Clear active process memory mapping
    if broadcast_id in BROADCAST_STATUS:
        del BROADCAST_STATUS[broadcast_id]


@Client.on_callback_query(filters.regex(r"^stop_brd_"))
async def cancel_broadcast_callback(bot: Client, callback_query: CallbackQuery):
    """Dynamic network hook engine to trigger absolute broadcast cancellation."""
    broadcast_id = int(callback_query.data.split("_")[2])
    
    if callback_query.from_user.id != Config.BOT_OWNER:
        await callback_query.answer("❌ Only Developer Ovesh can access this control vector!", show_alert=True)
        return

    if broadcast_id in BROADCAST_STATUS:
        BROADCAST_STATUS[broadcast_id]["run"] = False
        await callback_query.answer("🔄 Injection Sent: Terminating running loops...", show_alert=True)
    else:
        await callback_query.answer("⚠️ Session Expired or Broadcast already ended.", show_alert=True)
