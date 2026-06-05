
import asyncio 
from database import Db, db
from script import Script
from pyrogram import Client, filters
from .test import get_configs, update_configs, CLIENT, parse_buttons
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from .db import connect_user_db

CLIENT = CLIENT()



@Client.on_message(filters.command('settings'))
async def settings(client, message):
   buttons = await main_buttons(message.from_user.id)
   await message.reply_text(
     "<b>⚙️ <u>ADVANCED CONTROL PANEL</u>\n\nWelcome to your setup dashboard. Customize the bot behavior using the intuitive options below:</b>",
     reply_markup=buttons
   )

# Don't Remove Credit Tg - @Your_Username

@Client.on_callback_query(filters.regex(r'^settings'))
async def settings_query(bot, query):
  user_id = query.from_user.id
  _, type = query.data.split("#")
  buttons = [[InlineKeyboardButton('🔙 Back to Menu', callback_data="settings#main")]]
  
  if type == "main":
      markup = await main_buttons(user_id)
      await query.message.edit_text(
        "<b>⚙️ <u>ADVANCED CONTROL PANEL</u>\n\nWelcome to your setup dashboard. Customize the bot behavior using the intuitive options below:</b>",
        reply_markup=markup
      )
        
  elif type == "extra":
       markup = await extra_buttons(user_id)
       await query.message.edit_text(
          "<b>🧪 <u>EXTRA UTILITIES & LIMITS</u>\n\nFine-tune your file transfers by configuring advanced parameters:</b>",
          reply_markup=markup
       )
          
  elif type == "bots":
      # Parallel fetching to remove delays
      _bot, usr_bot = await asyncio.gather(db.get_bot(user_id), db.get_userbot(user_id))
      buttons = [] 
      
      text = "<b>🤖 <u>BOT MANAGEMENT HUB</u>\n\n"
      text += f"• Main Bot Status: {'🟢 Active' if _bot else '🔴 Not Connected'}\n"
      text += f"• Userbot Status: {'🟢 Active' if usr_bot else '🔴 Not Connected'}\n\n"
      text += "Manage your specialized automation layers:</b>"

      if _bot:
         buttons.append([InlineKeyboardButton(f"🤖 Edit: {_bot['name']}", callback_data="settings#editbot")])
      else:
         buttons.append([InlineKeyboardButton('➕ Link Bot Token', callback_data="settings#addbot")])
         
      if usr_bot:
         buttons.append([InlineKeyboardButton(f"👤 Edit Userbot: {usr_bot['name']}", callback_data="settings#edituserbot")])
      else:
         buttons.append([InlineKeyboardButton('➕ Link Telegram Userbot', callback_data="settings#adduserbot")])
         
      buttons.append([InlineKeyboardButton('🔙 Back', callback_data="settings#main")])
      await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(buttons))

  elif type == "addbot":
      await query.message.delete()
      bot_res = await CLIENT.add_bot(bot, query)
      if bot_res != True: return
      await query.message.reply_text(
         "<b>✅ Main Bot Token successfully updated in your Database!</b>",
         reply_markup=InlineKeyboardMarkup(buttons)
      )

  elif type == "adduserbot":
      await query.message.delete()
      user_res = await CLIENT.add_session(bot, query)
      if user_res != True: return
      await query.message.reply_text(
         "<b>✅ Userbot string session securely saved to DB!</b>",
         reply_markup=InlineKeyboardMarkup(buttons)
      )

  elif type == "channels":
      buttons = []
      channels = await db.get_user_channels(user_id)
      total_chats = len(channels) if channels else 0
      
      text = f"<b>📡 <u>TARGET CHANNELS MANAGER</u>\n\nTotal Configured Connections: <code>{total_chats}</code>\n\nSelect a channel to delete or add a new channel connection:</b>"
      
      if channels:
          for channel in channels:
             buttons.append([InlineKeyboardButton(f"🎯 {channel['title']}", callback_data=f"settings#editchannels_{channel['chat_id']}")])
             
      buttons.append([InlineKeyboardButton('➕ Deploy Target Chat', callback_data="settings#addchannel")])
      buttons.append([InlineKeyboardButton('🔙 Back', callback_data="settings#main")])
      await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(buttons))

  elif type == "addchannel":  
      await query.message.delete()
      chat_ids = await bot.ask(chat_id=query.from_user.id, text="<b>❪ 🎯 DEPLOY TARGET CHAT ❫\n\nForward a message from your target channel or group:\n\nSend /cancel to terminate setup.</b>")
      if chat_ids.text == "/cancel":
         return await chat_ids.reply_text(
                  "<b>❌ Operation aborted by user.</b>",
                  reply_markup=InlineKeyboardMarkup(buttons)
                )
      elif not chat_ids.forward_date:
         return await chat_ids.reply("<b>❌ Verification Failed! This is not a forwarded message. Process canceled.</b>")
      
      chat_id = chat_ids.forward_from_chat.id
      title = chat_ids.forward_from_chat.title
      username = chat_ids.forward_from_chat.username
      username = "@" + username if username else "private"
         
      chat = await db.add_channel(user_id, chat_id, title, username)
      await query.message.reply_text(
         "<b>✅ Channel integrated successfully!</b>" if chat else "<b>⚠️ Integration Alert: This destination is already configured!</b>",
         reply_markup=InlineKeyboardMarkup(buttons)
      )

  elif type == "editbot": 
      bot_data = await db.get_bot(user_id)
      TEXT = Script.BOT_DETAILS if bot_data['is_bot'] else Script.USER_DETAILS
      buttons = [[InlineKeyboardButton('🗑️ Terminate & Wipe Bot', callback_data="settings#removebot")],
                 [InlineKeyboardButton('🔙 Back', callback_data="settings#bots")]]
      await query.message.edit_text(
         TEXT.format(bot_data['name'], bot_data['id'], bot_data['username']),
         reply_markup=InlineKeyboardMarkup(buttons)
      )
       
  elif type == "edituserbot": 
      ubot_data = await db.get_userbot(user_id)
      TEXT = Script.USER_DETAILS
      buttons = [[InlineKeyboardButton('🗑️ Disconnect Userbot', callback_data="settings#removeuserbot")],
                 [InlineKeyboardButton('🔙 Back', callback_data="settings#bots")]]
      await query.message.edit_text(
         TEXT.format(ubot_data['name'], ubot_data['id'], ubot_data['username']),
         reply_markup=InlineKeyboardMarkup(buttons)
      )
       
  elif type == "removebot":
      await db.remove_bot(user_id)
      await query.message.edit_text("<b>🗑️ Main Bot details scrubbed from database successfully.</b>", reply_markup=InlineKeyboardMarkup(buttons))
       
  elif type == "removeuserbot":
      await db.remove_userbot(user_id)
      await query.message.edit_text("<b>🗑️ Userbot account decoupled and removed.</b>", reply_markup=InlineKeyboardMarkup(buttons))
       
  elif type.startswith("editchannels"): 
      chat_id = type.split('_')[1]
      chat = await db.get_channel_details(user_id, chat_id)
      buttons = [[InlineKeyboardButton('🗑️ Revoke Integration', callback_data=f"settings#removechannel_{chat_id}")],
                 [InlineKeyboardButton('🔙 Back', callback_data="settings#channels")]]
      await query.message.edit_text(
         f"<b>📄 <u>CHANNEL METADATA INSIGHTS</u>\n\n• Name:</b> <code>{chat['title']}</code>\n<b>• Chat ID:</b> <code>{chat['chat_id']}</code>\n<b>• Handle:</b> {chat['username']}",
         reply_markup=InlineKeyboardMarkup(buttons)
      )

  elif type.startswith("removechannel"):
      chat_id = type.split('_')[1]
      await db.remove_channel(user_id, chat_id)
      await query.message.edit_text("<b>🗑️ Destination link severed and removed.</b>", reply_markup=InlineKeyboardMarkup(buttons))

  elif type == "caption":
      buttons = []
      data = await get_configs(user_id)
      caption = data['caption']
      if caption is None:
         buttons.append([InlineKeyboardButton('➕ Add Custom Caption', callback_data="settings#addcaption")])
      else:
         buttons.append([InlineKeyboardButton('👁️ View Design', callback_data="settings#seecaption")])
         buttons[-1].append(InlineKeyboardButton('🗑️ Delete', callback_data="settings#deletecaption"))
      buttons.append([InlineKeyboardButton('🔙 Back', callback_data="settings#main")])
      
      await query.message.edit_text(
         "<b>📝 <u>DYNAMIC CAPTION STUDIO</u>\n\nInject your specialized layout configurations into all ongoing transfers.\n\n<u>SUPPORTED ARGUMENTS:</u>\n• <code>{filename}</code> - Target File Title\n• <code>{size}</code> - Computed Data Size\n• <code>{caption}</code> - Original Asset Context</b>",
         reply_markup=InlineKeyboardMarkup(buttons)
      )

  elif type == "seecaption":   
      data = await get_configs(user_id)
      buttons = [[InlineKeyboardButton('📝 Overwrite Design', callback_data="settings#addcaption")],
                 [InlineKeyboardButton('🔙 Back', callback_data="settings#caption")]]
      await query.message.edit_text(
         f"<b>📋 <u>CURRENT CAPTION SCHEMA</u>\n\n<code>{data['caption']}</code></b>",
         reply_markup=InlineKeyboardMarkup(buttons)
      )

  elif type == "deletecaption":
      await update_configs(user_id, 'caption', None)
      await query.message.edit_text("<b>🗑️ Custom templates removed. Reverting to default captions.</b>", reply_markup=InlineKeyboardMarkup(buttons))

  elif type == "addcaption":
      await query.message.delete()
      caption = await bot.ask(query.message.chat.id, "<b>✍️ Send your desired template structural text:\n\nSend /cancel to terminate layout session.</b>")
      if caption.text == "/cancel":
         return await caption.reply_text("<b>❌ Layout configuration session killed.</b>", reply_markup=InlineKeyboardMarkup(buttons))
      try:
          caption.text.format(filename='', size='', caption='')
      except KeyError as e:
          return await caption.reply_text(f"<b>❌ Formatting Fault! Unknown variable placeholder used: {e}. Recheck syntax and retry.</b>", reply_markup=InlineKeyboardMarkup(buttons))
      await update_configs(user_id, 'caption', caption.text)
      await caption.reply_text("<b>✅ Structural templates configured successfully!</b>", reply_markup=InlineKeyboardMarkup(buttons))

  elif type == "button":
      buttons = []
      button = (await get_configs(user_id))['button']
      if button is None:
         buttons.append([InlineKeyboardButton('➕ Inject Custom Button', callback_data="settings#addbutton")])
      else:
         buttons.append([InlineKeyboardButton('👁️ Audit Buttons', callback_data="settings#seebutton")])
         buttons[-1].append(InlineKeyboardButton('🗑️ Wipe Configuration', callback_data="settings#deletebutton"))
      buttons.append([InlineKeyboardButton('🔙 Back', callback_data="settings#main")])
      await query.message.edit_text(
         "<b>🔘 <u>URL BUTTON INTERFACES</u>\n\nMap custom interactive inline buttons underneath every pushed feed asset.\n\n<u>STANDARD COMPILATION FORMAT:</u>\n<code>[Button Text][buttonurl:https://t.me/your_link]</code></b>",
         reply_markup=InlineKeyboardMarkup(buttons)
      )

  elif type == "addbutton":
      await query.message.delete()
      ask = await bot.ask(user_id, text="<b>✍️ Send your structural inline button raw matrix payload.\n\n<u>Syntax Template:</u>\n<code>[Updates Channel][buttonurl:https://t.me/Your_Channel]</code></b>")
      button = parse_buttons(ask.text.html)
      if not button:
         return await ask.reply("<b>❌ Parsing Error: Input validation failed due to broken syntax parameters.</b>")
      await update_configs(user_id, 'button', ask.text.html)
      await ask.reply("<b>✅ URL Component matrix integrated successfully!</b>", reply_markup=InlineKeyboardMarkup(buttons))

  elif type == "seebutton":
       button = (await get_configs(user_id))['button']
       button = parse_buttons(button, markup=False)
       button.append([InlineKeyboardButton("🔙 Back to Base", "settings#button")])
       await query.message.edit_text("<b>🎭 <u>LIVE COMPONENT PREVIEW</u>\n\nYour button array translates exactly as configured below:</b>", reply_markup=InlineKeyboardMarkup(button))

  elif type == "deletebutton":
      await update_configs(user_id, 'button', None)
      await query.message.edit_text("<b>🗑️ All button component attachments flushed from system memory.</b>", reply_markup=InlineKeyboardMarkup(buttons))

  elif type == "database":
      buttons = []
      db_uri = (await get_configs(user_id))['db_uri']
      if db_uri is None:
         buttons.append([InlineKeyboardButton('➕ Connect Mongo Cluster', callback_data="settings#addurl")])
      else:
         buttons.append([InlineKeyboardButton('👁️ Reveal Cluster URI', callback_data="settings#seeurl")])
         buttons[-1].append(InlineKeyboardButton('⚠️ Detach DB Connection', callback_data="settings#deleteurl"))
      buttons.append([InlineKeyboardButton('🔙 Back', callback_data="settings#main")])
      await query.message.edit_text(
         "<b>🗃️ <u>DEDICATED MONGO STORAGE</u>\n\nA custom engine ensures historical lookup configurations, duplicate indexing data, and task metrics persist seamlessly across system cycles. Without a linked DB, cached datasets dissolve upon instance reload.</b>",
         reply_markup=InlineKeyboardMarkup(buttons)
      )

  elif type == "addurl":
      await query.message.delete()
      uri = await bot.ask(user_id, "<b>✍️ Provide your authenticated MongoDB Atlas Connection URI String:</b>\n\n<i>Generate credentials seamlessly inside cloud platform infrastructure dashboard at mongodb.com</i>", disable_web_page_preview=True)
      if uri.text == "/cancel":
         return await uri.reply_text("<b>❌ DB configuration session killed.</b>", reply_markup=InlineKeyboardMarkup(buttons))
      if not uri.text.startswith("mongodb+srv://"):
         return await uri.reply("<b>❌ Malformed Error: Protocol schema must align with authenticated <code>mongodb+srv://</code> cloud endpoint string values.</b>", reply_markup=InlineKeyboardMarkup(buttons))
      
      connect, udb = await connect_user_db(user_id, uri.text, "test")
      if connect:
         await udb.drop_all()
         await udb.close()
      else:
         return await uri.reply("<b>❌ Handshake Failed: System timed out trying to authenticate connection with specified cloud credentials. Check access permissions.</b>", reply_markup=InlineKeyboardMarkup(buttons))
      await update_configs(user_id, 'db_uri', uri.text)
      await uri.reply("<b>✅ Remote Database connected and synced successfully!</b>", reply_markup=InlineKeyboardMarkup(buttons))

  elif type == "seeurl":
      db_uri = (await get_configs(user_id))['db_uri']
      await query.answer(f"🔐 ACTIVE CLUSTER ENDPOINT:\n\n{db_uri}", show_alert=True)

  elif type == "deleteurl":
      await update_configs(user_id, 'db_uri', None)
      await query.message.edit_text("<b>🗑️ Custom cluster credentials erased from database configurations safely.</b>", reply_markup=InlineKeyboardMarkup(buttons))

  elif type == "filters":
      markup = await filters_buttons(user_id)
      await query.message.edit_text(
         "<b>💠 <u>ROUTING CONTENT FILTERS (PAGE 1)</u>\n\nTweak engine mechanics to explicitly pass or block specific media variations:</b>",
         reply_markup=markup
      )

  elif type == "nextfilters":
      markup = await next_filters_buttons(user_id)
      await query.edit_message_reply_markup(reply_markup=markup)

  elif type.startswith("updatefilter"):
      _, key, value = type.split('-')
      await update_configs(user_id, key, value != "True")
      
      if key in ['poll', 'protect', 'voice', 'animation', 'sticker', 'duplicate']:
         markup = await next_filters_buttons(user_id)
      else:
         markup = await filters_buttons(user_id)
      await query.edit_message_reply_markup(reply_markup=markup)

  elif type.startswith("file_size"):
    settings_data = await get_configs(user_id)
    size = settings_data.get('min_size', 0)
    await query.message.edit_text(
       f'<b>📉 <u>LOWER CONSTRAINT THRESHOLD</u>\n\nIgnore under-sized asset packets. Files larger than <code>{size} MB</code> will pass system gates.</b>',
       reply_markup=size_button(size)
    )
      
  elif type.startswith("maxfile_size"):
    settings_data = await get_configs(user_id)
    size = settings_data.get('max_size', 0)
    await query.message.edit_text(
       f'<b>📈 <u>UPPER CONSTRAINT THRESHOLD</u>\n\nProtect memory channels from data flooding. Files smaller than <code>{size} MB</code> will process down channels.</b>',
       reply_markup=maxsize_button(size)
    )

  elif type.startswith("update_size"):
    size = int(query.data.split('-')[1])
    if 0 < size > 4000:
       return await query.answer("🚨 Size boundary constraint breach! System limits values strictly within 0-4000MB caps.", show_alert=True)
    await update_configs(user_id, 'min_size', size)
    await query.message.edit_text(
       f'<b>📉 <u>LOWER CONSTRAINT THRESHOLD</u>\n\nIgnore under-sized asset packets. Files larger than <code>{size} MB</code> will pass system gates.</b>',
       reply_markup=size_button(size)
    )
      
  elif type.startswith("maxupdate_size"):
    size = int(query.data.split('-')[1])
    if 0 < size > 4000:
       return await query.answer("🚨 Size boundary constraint breach! System limits values strictly within 0-4000MB caps.", show_alert=True)
    await update_configs(user_id, 'max_size', size)
    await query.message.edit_text(
       f'<b>📈 <u>UPPER CONSTRAINT THRESHOLD</u>\n\nProtect memory channels from data flooding. Files smaller than <code>{size} MB</code> will process down channels.</b>',
       reply_markup=maxsize_button(size)
    )

  elif type.startswith('update_limit'):
     _, limit, size = type.split('-')
     limit, sts = size_limit(limit)
     await update_configs(user_id, 'size_limit', limit) 
     await query.message.edit_text(
        f'<b>📐 <u>CRITERIA EVALUATION TUNER</u>\n\nActive Filter Status: All incoming files measuring {sts} <code>{size} MB</code> will proceed.</b>',
        reply_markup=size_button(int(size))
     )

  elif type == "add_extension":
     await query.message.delete() 
     ext = await bot.ask(user_id, text="<b>✍️ Provide blacklisted file extension string patterns divided by blank spacing.\n\n<u>Example Profile:</u> <code>mkv mp4 zip m3u8</code></b>")
     if ext.text == '/cancel':
        return await ext.reply_text("<b>❌ Extension update cancelled.</b>", reply_markup=InlineKeyboardMarkup(buttons))
     extensions = ext.text.split(" ")
     extension = (await get_configs(user_id))['extension']
     if extension:
         extension.extend(extensions)
     else:
         extension = extensions
     await update_configs(user_id, 'extension', extension)
     buttons = [[InlineKeyboardButton('🔙 Back', callback_data="settings#get_extension")]]
     await ext.reply_text("<b>✅ Extension parameters appended into local system blacklists successfully!</b>", reply_markup=InlineKeyboardMarkup(buttons))

  elif type == "get_extension":
     extensions = (await get_configs(user_id))['extension']
     btn = []
     text = ""
     if extensions:
        text += "<b>⚡ BLOCKED EXTENSIONS LIST:</b>"
        for ext in extensions:
           text += f"\n• <code>.{ext}</code>"
     else:
        text += "<b>🟢 Clean Ledger: No extension restrictions currently enforced.</b>"
     btn.append([InlineKeyboardButton('➕ Add Extensions', 'settings#add_extension')])
     btn.append([InlineKeyboardButton('🧹 Wipe All Entries', 'settings#rmve_all_extension')])
     btn.append([InlineKeyboardButton('🔙 Back', 'settings#extra')])
     await query.message.edit_text(
         text=f"<b>🕹️ <u>EXTENSION FILTERS LAB</u>\n\nAssets matching matching these formats will be skipped instantly:\n\n{text}</b>",
         reply_markup=InlineKeyboardMarkup(btn)
     )

  elif type == "rmve_all_extension":
     await update_configs(user_id, 'extension', None)
     buttons = [[InlineKeyboardButton('🔙 Back', callback_data="settings#get_extension")]]
     await query.message.edit_text(text="<b>🧹 Blacklisted extension criteria dropped entirely. Ledger is clean now.</b>", reply_markup=InlineKeyboardMarkup(buttons))

  elif type == "add_keyword":
     await query.message.delete()
     ask = await bot.ask(user_id, text="<b>✍️ Provide your target lookup terms separated by standard space configurations.\n\n<u>Example Pattern:</u> <code>1080p WebRip English HEVC</code></b>")
     if ask.text == '/cancel':
        return await ask.reply_text("<b>❌ Keyword processing engine terminated.</b>", reply_markup=InlineKeyboardMarkup(buttons))
     keywords = ask.text.split(" ")
     keyword = (await get_configs(user_id))['keywords']
     if keyword:
         keyword.extend(keywords)
     else:
         keyword = keywords
     await update_configs(user_id, 'keywords', keyword)
     buttons = [[InlineKeyboardButton('🔙 Back', callback_data="settings#get_keyword")]]
     await ask.reply_text("<b>✅ Targets successfully locked onto local configuration indexes!</b>", reply_markup=InlineKeyboardMarkup(buttons))

  elif type == "get_keyword":
     keywords = (await get_configs(user_id))['keywords']
     btn = []
     text = ""
     if keywords:
        text += "<b>🎯 ACTIVE WHITELIST RULES:</b>"
        for key in keywords:
           text += f"\n• <code>{key}</code>"
     else:
        text += "<b>⚠️ Open Routing: No conditional keywords applied. System accepts all names.</b>"
     btn.append([InlineKeyboardButton('➕ Inject Keywords', 'settings#add_keyword')])
     btn.append([InlineKeyboardButton('🧹 Flush All Rules', 'settings#rmve_all_keyword')])
     btn.append([InlineKeyboardButton('🔙 Back', 'settings#extra')])
     await query.message.edit_text(
         text=f"<b>🔖 <u>KEYWORD REGEX ROUTER</u>\n\nOnly files containing these explicitly defined phrase sequences will be forwarded:\n\n{text}</b>",
         reply_markup=InlineKeyboardMarkup(btn)
     )

  elif type == "rmve_all_keyword":
     await update_configs(user_id, 'keywords', None)
     buttons = [[InlineKeyboardButton('🔙 Back', callback_data="settings#get_keyword")]]
     await query.message.edit_text(text="<b>🧹 Whitelist terms purged entirely from local tracking indexes.</b>", reply_markup=InlineKeyboardMarkup(buttons))

  elif type.startswith("alert"):
     alert = type.split('_')[1]
     await query.answer(alert, show_alert=True)

# Don't Remove Credit Tg - @Your_Username

async def extra_buttons(user_id):
   config = await get_configs(user_id)
   kw_count = len(config.get('keywords', [])) if config.get('keywords') else 0
   ext_count = len(config.get('extension', [])) if config.get('extension') else 0
   
   buttons = [[
       InlineKeyboardButton('📉 Min Size Threshold', callback_data='settings#file_size')
       ],[
       InlineKeyboardButton('📈 Max Size Threshold', callback_data='settings#maxfile_size')
       ],[
       InlineKeyboardButton(f'🚥 Keywords ({kw_count})', callback_data='settings#get_keyword'),
       InlineKeyboardButton(f'🕹️ Extensions ({ext_count})', callback_data='settings#get_extension')
       ],[
       InlineKeyboardButton('🔙 Back to Main Menu', callback_data='settings#main')
       ]]
   return InlineKeyboardMarkup(buttons)

# Don't Remove Credit Tg - @Your_Username

async def main_buttons(user_id):
  # Optimized concurrent fetching execution
  _bot, usr_bot, channels, config = await asyncio.gather(
      db.get_bot(user_id),
      db.get_userbot(user_id),
      db.get_user_channels(user_id),
      get_configs(user_id)
  )
  
  bot_count = sum(1 for x in [_bot, usr_bot] if x is not None)
  chan_count = len(channels) if channels else 0
  db_status = "🟢 ON" if config.get('db_uri') else "🔴 OFF"
  cap_status = "✅ ON" if config.get('caption') else "❌ OFF"
  btn_status = "✅ ON" if config.get('button') else "❌ OFF"

  buttons = [[
       InlineKeyboardButton(f'🤖 Bots Hub ({bot_count})', callback_data='settings#bots'),
       InlineKeyboardButton(f'📡 Channels ({chan_count})', callback_data='settings#channels')
       ],[
       InlineKeyboardButton(f'📝 Caption: {cap_status}', callback_data='settings#caption'),
       InlineKeyboardButton(f'🔘 Buttons: {btn_status}', callback_data='settings#button')
       ],[
       InlineKeyboardButton('🕵️‍♂️ Media Filter Matrix 🕵️‍♂️', callback_data='settings#filters')
       ],[
       InlineKeyboardButton(f'🗃️ DB Identity Cluster: {db_status}', callback_data='settings#database')
       ],[
       InlineKeyboardButton('🧪 Advanced Utilities Laboratory 🧪', callback_data='settings#extra')
       ],[
       InlineKeyboardButton('🚪 Close Dashboard', callback_data='help')
       ]]
  return InlineKeyboardMarkup(buttons)

# Don't Remove Credit Tg - @Your_Username

def size_limit(limit):
   if str(limit) == "None":
      return None, ""
   return (True, "more than") if str(limit) == "True" else (False, "less than")

def extract_btn(datas):
    i = 0
    btn = []
    if datas:
       for data in datas:
         if i >= 3:
            i = 0
         if i == 0:
            btn.append([InlineKeyboardButton(data, f'settings#alert_{data}')])
            i += 1
         elif i > 0:
            btn[-1].append(InlineKeyboardButton(data, f'settings#alert_{data}'))
            i += 1
    return btn 

def maxsize_button(size):
  return InlineKeyboardMarkup([[
       InlineKeyboardButton('📈 Configure Max Size Limit', callback_data='noth')
       ],[
       InlineKeyboardButton('+1 MB', callback_data=f'settings#maxupdate_size-{size + 1}'),
       InlineKeyboardButton('-1 MB', callback_data=f'settings#maxupdate_size-{size - 1}')
       ],[
       InlineKeyboardButton('+5 MB', callback_data=f'settings#maxupdate_size-{size + 5}'),
       InlineKeyboardButton('-5 MB', callback_data=f'settings#maxupdate_size-{size - 5}')
       ],[
       InlineKeyboardButton('+10 MB', callback_data=f'settings#maxupdate_size-{size + 10}'),
       InlineKeyboardButton('-10 MB', callback_data=f'settings#maxupdate_size-{size - 10}')
       ],[
       InlineKeyboardButton('+50 MB', callback_data=f'settings#maxupdate_size-{size + 50}'),
       InlineKeyboardButton('-50 MB', callback_data=f'settings#maxupdate_size-{size - 50}')
       ],[
       InlineKeyboardButton('+100 MB', callback_data=f'settings#maxupdate_size-{size + 100}'),
       InlineKeyboardButton('-100 MB', callback_data=f'settings#maxupdate_size-{size - 100}')
       ],[
       InlineKeyboardButton('🔙 Back', callback_data="settings#extra")
     ]])

def size_button(size):
  return InlineKeyboardMarkup([[
       InlineKeyboardButton('📉 Configure Min Size Limit', callback_data='noth')
       ],[
       InlineKeyboardButton('+1 MB', callback_data=f'settings#update_size-{size + 1}'),
       InlineKeyboardButton('-1 MB', callback_data=f'settings#update_size-{size - 1}')
       ],[
       InlineKeyboardButton('+5 MB', callback_data=f'settings#update_size-{size + 5}'),
       InlineKeyboardButton('-5 MB', callback_data=f'settings#update_size-{size - 5}')
       ],[
       InlineKeyboardButton('+10 MB', callback_data=f'settings#update_size-{size + 10}'),
       InlineKeyboardButton('-10 MB', callback_data=f'settings#update_size-{size - 10}')
       ],[
       InlineKeyboardButton('+50 MB', callback_data=f'settings#update_size-{size + 50}'),
       InlineKeyboardButton('-50 MB', callback_data=f'settings#update_size-{size - 50}')
       ],[
       InlineKeyboardButton('+100 MB', callback_data=f'settings#update_size-{size + 100}'),
       InlineKeyboardButton('-100 MB', callback_data=f'settings#update_size-{size - 100}')
       ],[
       InlineKeyboardButton('🔙 Back', callback_data="settings#extra")
     ]])

async def filters_buttons(user_id):
  filter_data = await get_configs(user_id)
  filters = filter_data['filters']
  return InlineKeyboardMarkup([[
       InlineKeyboardButton('🏷️ Forward Original Tag', callback_data=f'settings_#updatefilter-forward_tag-{filter_data["forward_tag"]}'),
       InlineKeyboardButton('✅' if filter_data['forward_tag'] else '❌', callback_data=f'settings#updatefilter-forward_tag-{filter_data["forward_tag"]}')
       ],[
       InlineKeyboardButton('🖍️ Plain Text Messages', callback_data=f'settings_#updatefilter-text-{filters["text"]}'),
       InlineKeyboardButton('✅' if filters['text'] else '❌', callback_data=f'settings#updatefilter-text-{filters["text"]}')
       ],[
       InlineKeyboardButton('📁 Raw Documents', callback_data=f'settings_#updatefilter-document-{filters["document"]}'),
       InlineKeyboardButton('✅' if filters['document'] else '❌', callback_data=f'settings#updatefilter-document-{filters["document"]}')
       ],[
       InlineKeyboardButton('🎞️ Video Files Stream', callback_data=f'settings_#updatefilter-video-{filters["video"]}'),
       InlineKeyboardButton('✅' if filters['video'] else '❌', callback_data=f'settings#updatefilter-video-{filters["video"]}')
       ],[
       InlineKeyboardButton('📷 Image Assets', callback_data=f'settings_#updatefilter-photo-{filters["photo"]}'),
       InlineKeyboardButton('✅' if filters['photo'] else '❌', callback_data=f'settings#updatefilter-photo-{filters["photo"]}')
       ],[
       InlineKeyboardButton('🎧 Audio Soundtracks', callback_data=f'settings_#updatefilter-audio-{filters["audio"]}'),
       InlineKeyboardButton('✅' if filters['audio'] else '❌', callback_data=f'settings#updatefilter-audio-{filters["audio"]}')
       ],[
       InlineKeyboardButton('🔙 Menu Base', callback_data="settings#main"),
       InlineKeyboardButton('Next Metrics ⏩', callback_data="settings#nextfilters")
       ]])

async def next_filters_buttons(user_id):
  filter_data = await get_configs(user_id)
  filters = filter_data['filters']
  return InlineKeyboardMarkup([[
       InlineKeyboardButton('🎤 Short Voice Notes', callback_data=f'settings_#updatefilter-voice-{filters["voice"]}'),
       InlineKeyboardButton('✅' if filters['voice'] else '❌', callback_data=f'settings#updatefilter-voice-{filters["voice"]}')
       ],[
       InlineKeyboardButton('🎭 GIF Animations', callback_data=f'settings_#updatefilter-animation-{filters["animation"]}'),
       InlineKeyboardButton('✅' if filters['animation'] else '❌', callback_data=f'settings#updatefilter-animation-{filters["animation"]}')
       ],[
       InlineKeyboardButton('🃏 Expressive Stickers', callback_data=f'settings_#updatefilter-sticker-{filters["sticker"]}'),
       InlineKeyboardButton('✅' if filters['sticker'] else '❌', callback_data=f'settings#updatefilter-sticker-{filters["sticker"]}')
       ],[
       InlineKeyboardButton('▶️ Fast Skip Duplicates', callback_data=f'settings_#updatefilter-duplicate-{filter_data["duplicate"]}'),
       InlineKeyboardButton('✅' if filter_data['duplicate'] else '❌', callback_data=f'settings#updatefilter-duplicate-{filter_data["duplicate"]}')
       ],[
       InlineKeyboardButton('📊 Interactive Polls', callback_data=f'settings_#updatefilter-poll-{filters["poll"]}'),
       InlineKeyboardButton('✅' if filters['poll'] else '❌', callback_data=f'settings#updatefilter-poll-{filters["poll"]}')
       ],[
       InlineKeyboardButton('🔒 Secure Forward Protection', callback_data=f'settings_#updatefilter-protect-{filter_data["protect"]}'),
       InlineKeyboardButton('✅' if filter_data['protect'] else '❌', callback_data=f'settings#updatefilter-protect-{filter_data["protect"]}')
       ],[
       InlineKeyboardButton('⏪ Page 1', callback_data="settings#filters"),
       InlineKeyboardButton('Finish Menu 🔚', callback_data="settings#main")
       ]])
