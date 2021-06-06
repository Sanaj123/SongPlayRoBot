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
    videosSearch = VideosSearch(song, limit=1)
    result = videosSearch.result()
    if not result:
        return False
    else:
        video_id = result["result"][0]["id"]
        url = f"https://youtu.be/{video_id}"
        return url


@app.on_message(filters.create(ignore_blacklisted_users) & filters.command("as"))
async def song(client, message):
    chat_id = message.chat.id
    user_id = message.from_user["id"]
    add_chat_to_db(str(chat_id))
    args = get_arg(message) + " " + "as"
    if args.startswith(" "):
        await message.reply("പാട്ടിന്റെ പേര് എനിക്ക് വ്യക്തമല്ല 😅. Check /help")
        return ""
    status = await message.reply("പാട്ട് ഞാൻ തിരയുന്നു.....🔎 ഇപ്പോൾ വരും കേട്ടോ.......🥰[💘](https://t.me/c/1288468141/3)")
    video_link = yt_search(args)
    if not video_link:
        await status.edit("എനിക്ക് തോന്നുന്നു താങ്കൾക്കു അക്ഷരം തെറ്റിയെന്ന്.വീണ്ടും ശ്രമിക്കു....❤.")
        return ""
    yt = YouTube(video_link)
    audio = yt.streams.filter(only_audio=True).first()
    try:
        download = audio.download(filename=f"{str(user_id)}")
    except Exception as ex:
        await status.edit("അവിടെയോ... എനിക്ക് തകരാർ സംഭവിച്ചു 😅. വീണ്ടും ശ്രമിക്കു...❤")
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
