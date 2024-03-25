import os
import time
import math
import json
import string
import random
import traceback
import asyncio
import datetime
import aiofiles
from random import choice

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid
from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid
from telegraph import upload_file
from database import Database


UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", "")
BOT_OWNER = int(os.environ["BOT_OWNER"])
DATABASE_URL = os.environ["DATABASE_URL"]
db = Database(DATABASE_URL, "TGraphRoBot")

Bot = Client(
    "Telegraph Uploader Bot",
    bot_token=os.environ["BOT_TOKEN"],
    api_id=int(os.environ["API_ID"]),
    api_hash=os.environ["API_HASH"],
)

DOWNLOAD_LOCATION = ("./DOWNLOADS/" + "doraemon890/Telegraph-Image")

START_TEXT = """ʜᴇʟʟᴏ {}

ɪ ᴀᴍ sᴍᴀʀᴛᴇsᴛ ʀᴏʙᴏᴛ ᴛʜᴀᴛ ᴄᴏɴᴠᴇʀᴛs ᴍᴇᴅɪᴀ ᴏʀ ғɪʟᴇ ᴛᴏ ᴛᴇʟᴇɢʀᴀᴘʜ ʟɪɴᴋ .

»  ɪᴡɪʟʟ ʜᴇʟᴘ ʏᴏᴜ ᴛᴏ ᴄᴏɴᴠᴇʀᴛ ᴜɴᴅᴇʀ 𝟻ᴍʙ ᴘʜᴏᴛᴏ ᴏʀ ᴠɪᴅᴇᴏ ᴛᴏ ᴛᴇʟᴇɢʀᴀᴘʜ ʟɪɴᴋ.

ᴛᴀᴘ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ᴏʀ ʜɪᴛ /ʜᴇʟᴘ ғᴏʀ ᴍᴏʀᴇ ɪɴғᴏ."""

HELP_TEXT = """ʜᴇʏ, ғᴏʟʟᴏᴡ ᴛʜᴇsᴇ sᴛᴇᴘs:

▷ ᴊᴜsᴛ sᴇɴᴅ ᴍᴇ ᴀ ᴍᴇᴅɪᴀ ᴜɴᴅᴇʀ 𝟻ᴍʙ.
▷ ᴛʜᴇɴ ɪ ᴡɪʟʟ ᴅᴏᴡɴʟᴏᴀᴅ ɪᴛ.
▷ 𝙰ғᴛᴇʀ ᴛʜᴀᴛ ɪ ᴡɪʟʟ ᴜᴘʟᴏᴀᴅ ɪᴛ ᴛᴏ ᴛʜᴇ ᴛᴇʟᴇɢʀᴀᴘʜ ʟɪɴᴋ.
"""

ABOUT_TEXT = """ᴀʙᴏᴜᴛ ᴍᴇ 🫧

🪽 ɴᴀᴍᴇ : [ᴛᴇʟᴇɢʀᴀᴘʜ ᴜᴘʟᴏᴀᴅᴇʀ](https://t.me/Telgraph_V2_Bot)

🪽 ᴅᴇᴠᴇʟᴏᴘᴇʀ : [ᴊᴀʀᴠɪs](https://t.me/JARVIS_V2)

🪽 Cʜᴀɴɴᴇʟ : [𝙹ᴀʀᴠɪs 𝚂ᴜᴘᴘᴏʀᴛ](https://t.me/JARVIS_X_SUPPORT)

🪽 ғᴇᴇᴅʙᴀᴄᴋ : [ᴛᴀᴘ ʜᴇʀᴇ](https://t.me/CHATTING_2024)

🪽 ʟᴀɴɢᴜᴀɢᴇ : [ᴘʏᴛʜᴏɴ³](https://python.org)

🪽 ғʀᴀᴍᴇᴡᴏʀᴋ : [ᴘʏʀᴏɢʀᴀᴍ](https://pyrogram.org)"""

START_BUTTONS = InlineKeyboardMarkup(
    [[
        InlineKeyboardButton('ᴥ︎︎︎ ʜᴇʟᴘ ᴥ︎︎︎', callback_data='help'),
        InlineKeyboardButton('🝮︎︎︎︎︎︎︎ ᴀʙᴏᴜᴛ 🝮︎︎︎︎︎︎︎', callback_data='about'),
    ],
     [
         InlineKeyboardButton('ꨄ︎ ᴄʟᴏsᴇ ꨄ︎', callback_data='close')
     ]]
)

HELP_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('𖤍 ʜᴏᴍᴇ 𖤍', callback_data='home'),
            InlineKeyboardButton('🝮︎︎︎︎︎︎︎ ᴀʙᴏᴜᴛ 🝮︎︎︎︎︎︎︎', callback_data='about')
        ],
        [
            InlineKeyboardButton('ꨄ︎ ᴄʟᴏsᴇ ꨄ︎', callback_data='close')
        ]
    ]
)


ABOUT_BUTTONS = InlineKeyboardMarkup(
    [[
        InlineKeyboardButton('𖤍 ʜᴏᴍᴇ 𖤍', callback_data='home'),
        InlineKeyboardButton('ᴥ︎︎︎ ʜᴇʟᴘ ᴥ︎︎︎', callback_data='help'),
    ],
     [
         InlineKeyboardButton('ꨄ︎ ᴄʟᴏsᴇ ꨄ︎', callback_data='close')
     ]]
)



async def send_msg(user_id, message):
    try:
        await message.copy(chat_id=user_id)
        return 200, None
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return send_msg(user_id, message)
    except InputUserDeactivated:
        return 400, f"{user_id} : deactivated\n"
    except UserIsBlocked:
        return 400, f"{user_id} : user is blocked\n"
    except PeerIdInvalid:
        return 400, f"{user_id} : user id invalid\n"
    except Exception as e:
        return 500, f"{user_id} : {traceback.format_exc()}\n"


@Bot.on_callback_query()
async def cb_handler(bot, update):
    if update.data == "home":
        await update.message.edit_text(
            text=START_TEXT.format(update.from_user.mention),
            reply_markup=START_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "help":
        await update.message.edit_text(
            text=HELP_TEXT,
            reply_markup=HELP_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TEXT.format((await bot.get_me()).username),
            reply_markup=ABOUT_BUTTONS,
            disable_web_page_preview=True
        )
    else:
        await update.message.delete()


@Bot.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    await update.reply_text(
        text=START_TEXT.format(update.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=START_BUTTONS
    )


@Bot.on_message(filters.private & filters.command(["help"]))
async def help(bot, update):
    await update.reply_text(
        text=HELP_TEXT,
        disable_web_page_preview=True,
        reply_markup=HELP_BUTTONS
    )


@Bot.on_message(filters.private & filters.command(["about"]))
async def about(bot, update):
    await update.reply_text(
        text=ABOUT_TEXT.format((await bot.get_me()).username),
        disable_web_page_preview=True,
        reply_markup=ABOUT_BUTTONS
    )

@Bot.on_message(filters.private & filters.media)
async def getmedia(bot, update):
    
    medianame = DOWNLOAD_LOCATION + str(update.from_user.id)
    
    try:
        message = await update.reply_text(
            text="`Processing...`",
            quote=True,
            disable_web_page_preview=True
        )
        await bot.download_media(
            message=update,
            file_name=medianame
        )
        response = upload_file(medianame)
        try:
            os.remove(medianame)
        except:
            pass
    except Exception as error:
        text=f"Error :- <code>{error}</code>"
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton('More Help', callback_data='help')]]
        )
        await message.edit_text(
            text=text,
            disable_web_page_preview=True,
            reply_markup=reply_markup
        )
        return
    
    text=f"**Link :-** `https://telegra.ph{response[0]}`\n\n**ᴘʟᴇᴀsᴇ ᴊᴏɪɴ 💗 :-** @JARVIS_X_SUPPORT"
    reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="ᴏᴘᴇɴ ʟɪɴᴋ 💗", url=f"https://telegra.ph{response[0]}"),
                InlineKeyboardButton(text="sʜᴀʀᴇ ʟɪɴᴋ🌷", url=f"https://telegram.me/share/url?url=https://telegra.ph{response[0]}")
            ],
            [
                InlineKeyboardButton(text="Jᴏɪɴ ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ🛠", url="https://telegram.me/JARVIS_X_SUPPORT")
            ]
        ]
    )
    
    await message.edit_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )

@Bot.on_message(filters.private & filters.command("broadcast") & filters.user(BOT_OWNER) & filters.reply)
async def broadcast(bot, update):
    broadcast_ids = {}
    all_users = await db.get_all_users()
    broadcast_msg = update.reply_to_message
    while True:
        broadcast_id = ''.join([random.choice(string.ascii_letters) for i in range(3)])
        if not broadcast_ids.get(broadcast_id):
            break
    out = await update.reply_text(text=f"ʙʀᴏᴀᴅᴄᴀsᴛ sᴛᴀʀᴛᴇᴅ! ʏᴏᴜ ᴡɪʟʟ ʙᴇ ɴᴏᴛɪғɪᴇᴅ ᴡɪᴛʜ ʟᴏɢ ғɪʟᴇ ᴡʜᴇɴ ᴀʟʟ ᴛʜᴇ ᴜsᴇʀs ᴀʀᴇ ɴᴏᴛɪғɪᴇᴅ.")

    start_time = time.time()
    total_users = await db.total_users_count()
    done = 0
    failed = 0
    success = 0
    broadcast_ids[broadcast_id] = dict(total=total_users, current=done, failed=failed, success=success)
    async with aiofiles.open('broadcast.txt', 'w') as broadcast_log_file:
        async for user in all_users:
            sts, msg = await send_msg(user_id=int(user['id']), message=broadcast_msg)
            if msg is not None:
                await broadcast_log_file.write(msg)
            if sts == 200:
                success += 1
            else:
                failed += 1
            if sts == 400:
                await db.delete_user(user['id'])
            done += 1
            if broadcast_ids.get(broadcast_id) is None:
                break
            else:
                broadcast_ids[broadcast_id].update(dict(current=done, failed=failed, success=success))
    if broadcast_ids.get(broadcast_id):
        broadcast_ids.pop(broadcast_id)
    completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
    await asyncio.sleep(3)
    await out.delete()
    if failed == 0:
        await update.reply_text(
            text=f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.",
            quote=True)
    else:
        await update.reply_document(
            document='broadcast.txt',
            caption=f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed."
        )
    os.remove('broadcast.txt')


@Bot.on_message(filters.private & filters.command("status"), group=5)
async def status(bot, update):
    total_users = await db.total_users_count()
    text = "**Bot Status**\n"
    text += f"\n**Total Users:** `{total_users}`"
    await update.reply_text(
        text=text,
        quote=True,
        disable_web_page_preview=True
    )


Bot.run()
