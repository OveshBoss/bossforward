import os
from config import Config

class Script(object):
    START_TXT = """<b>ʜɪ {}
  
ɪ'ᴍ ᴀɴ ᴀᴅᴠᴀɴᴄᴇᴅ ꜰᴏʀᴡᴀʀᴅ ʙᴏᴛ
ɪ ᴄᴀɴ ꜰᴏʀᴡᴀʀᴅ ᴀʟʟ ᴍᴇssᴀɢᴇs ꜰʀᴏᴍ ᴏɴᴇ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴀɴᴏᴛʜᴇʀ ᴄʜᴀɴɴᴇʟ ⚡</b>

**ᴄʟɪᴄᴋ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ᴛᴏ ᴋɴᴏᴡ ᴍᴏʀᴇ ᴀʙᴏᴜᴛ ᴍᴇ**"""

    HELP_TXT = """<b><u>🔆 Help Menu</u></b>

<u>**📚 Available Commands:**</u>
<b>⏣ __/start - Check if the bot is alive__ 
⏣ __/forward - Start forwarding messages__
⏣ __/settings - Configure your custom settings__
⏣ __/unequify - Delete duplicate media messages__
⏣ __/stop - Stop your ongoing tasks__
⏣ __/reset - Reset your settings to default__</b>

<b><u>💢 Features:</u></b>
<b>► __Forward messages from any public channel without admin permissions.__
► __If the source channel is private, userbot/bot needs to be a member.__
► __Custom text captions & custom buttons support.__
► __Skip duplicate messages automatically.__
► __Filter specific message types (Files, Photos, Videos etc.).__</b>"""
  
    HOW_USE_TXT = """<b><u>⚠️ Before Forwarding:</u></b>
<b>► __Add your bot or userbot to the bot settings.__
► __Make sure your bot/userbot is an admin in the Target Channel.__
► __You can easily manage chats or bots using /settings command.__
► __If the Source Channel is private, your userbot must be joined there.__
► __Once everything is set, use /forward to begin.__</b>"""
  
    ABOUT_TXT = """<b>
╔════❰ ғᴏʀᴡᴀʀᴅ ʙᴏᴛ ❱═❍⊱❁۪۪
║╭━━━━━━━━━━━━━━━➣
║┣⪼📃 ʙᴏᴛ : [ғᴏʀᴡᴀʀᴅ ʙᴏᴛ](https://t.me/your_bot_username)
║┣⪼👦 ᴄʀᴇᴀᴛᴏʀ : [ᴏᴡɴᴇʀ](https://t.me/your_telegram_id)
║┣⪼🤖 ᴜᴘᴅᴀᴛᴇs : [ᴄʜᴀɴɴᴇʟ](https://t.me/your_channel)
║┣⪼📡 ʜᴏsᴛᴇᴅ ᴏɴ : sᴜᴘᴇʀ ꜰᴀsᴛ sᴇʀᴠᴇʀ
║┣⪼🗣️ ʟᴀɴɢᴜᴀɢᴇ : ᴘʏᴛʜᴏɴ3
║┣⪼📚 ʟɪʙʀᴀʀʏ : ᴘʏʀᴏɢʀᴀᴍ ᴀsʏɴᴄ
║┣⪼🗒️ ᴠᴇʀsɪᴏɴ : 𝟸.𝟶.𝟶 (ᴀɪ ᴏᴘᴛɪᴍɪᴢᴇᴅ)
║╰━━━━━━━━━━━━━━━➣
╚══════════════════❍⊱❁۪۪
</b>"""

    STATUS_TXT = """
╔════❰ ʙᴏᴛ sᴛᴀᴛᴜs  ❱═❍⊱❁۪۪
║╭━━━━━━━━━━━━━━━➣
║┣⪼**⏳ ʙᴏᴛ ᴜᴘᴛɪᴍᴇ:** `{}`
║┃
║┣⪼**👱 Tᴏᴛᴀʟ Usᴇʀs:** `{}`
║┃
║┣⪼**🤖 Tᴏᴛᴀʟ Bᴏᴛs:** `{}`
║┃
║┣⪼**🔃 Fᴏʀᴡᴀʀᴅɪɴɢs:** `{}`
║┃
║╰━━━━━━━━━━━━━━━➣
╚══════════════════❍⊱❁۪۪
"""

    FROM_MSG = "<b>❪ SET SOURCE CHAT ❫\n\nForward the last message or last message link of the source chat.\n\n👉 Use /cancel to stop this process</b>"
    TO_MSG = "<b>❪ CHOOSE TARGET CHAT ❫\n\nChoose your target chat from the given buttons below.\n\n👉 Use /cancel to stop this process</b>"
    SKIP_MSG = "<b>❪ SET MESSAGE SKIPPING NUMBER ❫</b>\n\n<b>Enter the number of messages you want to skip. The rest will be forwarded.\n\nDefault Skip Number =</b> <code>0</code>\n<code>e.g., If you enter 5 = first 5 messages will be skipped</code>\n\n👉 Use /cancel to stop this process"
    CANCEL = "<b>❌ Process Cancelled Successfully!</b>"
    BOT_DETAILS = "<b><u>📄 BOT DETAILS</b></u>\n\n<b>➣ NAME:</b> <code>{}</code>\n<b>➣ BOT ID:</b> <code>{}</code>\n<b>➣ USERNAME:</b> @{}"
    USER_DETAILS = "<b><u>📄 USERBOT DETAILS</b></u>\n\n<b>➣ NAME:</b> <code>{}</code>\n<b>➣ USER ID:</b> <code>{}</code>\n<b>➣ USERNAME:</b> @{}"  
         
    TEXT = """
╔════❰ ꜰᴏʀᴡᴀʀᴅ sᴛᴀᴛᴜs ⚡ ❱═❍⊱❁۪۪
║╭━━━━━━━━━━━━━━━➣
║┣⪼ 📊 <b>ᴄᴜʀʀᴇɴᴛ sᴛᴀᴛᴜs:</b> <code>{}</code>
║┃
║┣⪼ 🔎 <b>ꜰᴇᴛᴄʜᴇᴅ ᴍsɢ:</b> <code>{}</code>
║┣⪼ 🆔 <b>ᴄᴜʀʀᴇɴᴛ ɪᴅ:</b> <code>{}</code>
║┃
║┣⪼ ✅ <b>sᴜᴄᴄᴇssꜰᴜʟʟʏ ꜰᴡᴅ:</b> <code>{}</code>
║┣⪼ 👥 <b>ᴅᴜᴘʟɪᴄᴀᴛᴇ sᴋɪᴘ:</b> <code>{}</code>
║┣⪼ 🪆 <b>ᴜsᴇʀ sᴋɪᴘᴘᴇᴅ:</b> <code>{}</code>
║┣⪼ 🔁 <b>ꜰɪʟᴛᴇʀᴇᴅ ᴏᴜᴛ:</b> <code>{}</code>
║┣⪼ 🗑 <b>ᴅᴇʟᴇᴛᴇᴅ ᴍsɢ:</b> <code>{}</code>
║┣⪼ ⚠️ <b>ꜰᴀɪʟᴇᴅ/ᴇʀʀᴏʀs:</b> <code>{}</code>
║┃
║┣⪼ 🚀 <b>ꜰᴏʀᴡᴀʀᴅ sᴘᴇᴇᴅ:</b> <code>{} msgs/sec</code>
║┣⪼ ⏳ <b>ᴛɪᴍᴇ ʀᴇᴍᴀɪɴɪɴɢ (ᴇᴛᴀ):</b> <code>{}</code>
║┃
║┣⪼ 📈 <b>ᴘᴇʀᴄᴇɴᴛᴀɢᴇ:</b> <code>{} %</code>
║┃
║┣⪼ 🔄 <b>ʟᴀsᴛ ᴜᴘᴅᴀᴛᴇᴅ:</b> <code>{}</code>
║╰━━━━━━━━━━━━━━━➣ 
╚════❰ sᴜᴘᴇʀ ꜰᴀsᴛ ᴇɴɢɪɴᴇ ❱══❍⊱❁۪۪
"""

    DUPLICATE_TEXT = """
╔════❰ ᴜɴᴇǫᴜɪꜰʏ sᴛᴀᴛᴜs ❱═❍⊱❁۪۪
║╭━━━━━━━━━━━━━━━➣
║┣⪼ <b>ꜰᴇᴛᴄʜᴇᴅ ꜰɪʟᴇs:</b> <code>{}</code>
║┃
║┣⪼ <b>ᴅᴜᴘʟɪᴄᴀᴛᴇ ᴅᴇʟᴇᴛᴇᴅ:</b> <code>{}</code> 
║╰━━━━━━━━━━━━━━━➣
╚════❰ ᴄʟᴇᴀɴ sᴜᴄᴄᴇss ❱══❍⊱❁۪۪
"""

    DOUBLE_CHECK = """<b><u>DOUBLE CHECKING ⚠️</u></b>
<code>Before starting the task, please verify the following details:</code>

<b>★ YOUR BOT:</b> [{botname}](t.me/{botuname})
<b>★ FROM CHANNEL:</b> `{from_chat}`
<b>★ TO CHANNEL:</b> `{to_chat}`
<b>★ SKIP MESSAGES:</b> `{skip}`

<i>° Make sure [{botname}](t.me/{botuname}) is an ADMIN in target chat (`{to_chat}`)</i>
<i>° If the source chat is private, your userbot must be a member there.</i>

<b>If everything looks correct, click the YES button below to start.</b>"""
  
    SETTINGS_TXT = """<b>Modify and configure your preferences below:</b>"""
