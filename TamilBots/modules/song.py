from pyrogram import Client, filters
import asyncio
import os
from pytube import YouTube
from pyrogram.types import InlineKeyboardMarkup
from pyrogram.types import InlineKeyboardButton
from youtubesearchpython import VideosSearch
from TamilBots.TamilBots import ignore_blacklisted_users, get_arg
from TamilBots import app, LOGGER
from TamilBots.sql.chat_sql import add_chat_to_db


def yt_search(song):
    videosSearch = VideosSearch(as, limit=1)
    result = videosSearch.result()
    if not result:
        return False
    else:
        video_id = result["result"][0]["id"]
        url = f"https://youtu.be/{video_id}"
        return url


@app.on_message(filters.create(ignore_blacklisted_users) & filters.command("song"))
async def song(client, message):
    chat_id = message.chat.id
    user_id = message.from_user["id"]
    add_chat_to_db(str(chat_id))
    args = get_arg(message) + " " + "as"
    if args.startswith(" "):
        await message.reply("Enter a song name. Check /help")
        return ""
    status = await message.reply("𝙔𝙤𝙪'𝙧𝙚 𝙨𝙚𝙖𝙧𝙘𝙝𝙞𝙣𝙜 𝙊𝙣 𝘼𝙎 𝙈𝙐𝙎𝙄𝘾.𝚙𝚕𝚎𝚊𝚜𝚎 𝚠𝚊𝚒𝚝[💖](https://t.me/As_github/5)")
    video_link = yt_search(args)
    if not video_link:
        await status.edit("I think this spelling are mistake. checkout and Retry ❤.")
        return ""
    yt = YouTube(video_link)
    audio = yt.streams.filter(only_audio=True).first()
    try:
        download = audio.download(filename=f"{str(user_id)}")
    except Exception as ex:
        await status.edit("Retry please ❤")
        LOGGER.error(ex)
        return ""
    rename = os.rename(download, f"{str(user_id)}.mp3")
    await app.send_chat_action(message.chat.id, "upload_audio")
    await app.send_audio(
        chat_id=message.chat.id,
        audio=f"{str(user_id)}.mp3",
        duration=int(yt.length),
        title=str(yt.title),
        performer=str(yt.title),
        reply_to_message_id=message.message_id,
    )
    await status.delete()
    os.remove(f"{str(user_id)}.mp3")
