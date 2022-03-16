# Copyright (C) 2021 By Akshi Music-Project
# Commit Start Date 20/10/2021
# Finished On 28/10/2021


# pyrogram stuff
from pyrogram import Client
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, Message
# pytgcalls stuff
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio
# repository stuff
from program.utils.inline import stream_markup
from driver.design.thumbnail import thumb
from driver.design.chatname import CHAT_TITLE
from driver.filters import command, other_filters
from driver.queues import QUEUE, add_to_queue
from driver.Akshi import call_py, user
from driver.utils import bash
from config import BOT_USERNAME, IMG_1, IMG_2
# youtube-dl stuff
from youtubesearchpython import VideosSearch


def ytsearch(query: str):
    try:
        search = VideosSearch(query, limit=1).result()
        data = search["result"][0]
        songname = data["title"]
        url = data["link"]
        duration = data["duration"]
        thumbnail = f"https://i.ytimg.com/vi/{data['id']}/hqdefault.jpg"
        return [songname, url, duration, thumbnail]
    except Exception as e:
        print(e)
        return 0


async def ytdl(link: str):
    stdout, stderr = await bash(
        f'yt-dlp -g -f "best[height<=?720][width<=?1280]" {link}'
    )
    if stdout:
        return 1, stdout
    return 0, stderr


@Client.on_message(command(["play", f"play@{BOT_USERNAME}"]) & other_filters)
async def play(c: Client, m: Message):
    await m.delete()
    replied = m.reply_to_message
    chat_id = m.chat.id
    user_id = m.from_user.id
    if m.sender_chat:
        return await m.reply_text(
            "**sen bir __Anonim__ Yöneticisisin !\n\n» yönetici haklarından kullanıcı hesabına geri dön.**"
        )
    try:
        aing = await c.get_me()
    except Exception as e:
        return await m.reply_text(f"error:\n\n{e}")
    a = await c.get_chat_member(chat_id, aing.id)
    if a.status != "administrator":
        await m.reply_text(
            f"💡 Beni kullanmak için, aşağıdaki izinlere sahip bir Yönetici olmam gerekiyor:\n\n» ❌ Mesajı sil\n» ❌ Kullanıcıları ekle\n» ❌ Vi sohbeti yönet\n\nİşiniz bittiğinde, /yeniden yükle" yazın"
        )
        return
    if not a.can_manage_voice_chats:
        await m.reply_text(
            "💡 Beni kullanmak için, bana aşağıdaki izni verin:"
            + "\n\n» ❌ Vi sohbeti yönet\n\nİşiniz bittiğinde tekrar deneyin."
        )
        return
    if not a.can_delete_messages:
        await m.reply_text(
            "💡 Beni kullanmak için, bana aşağıdaki izni verin:"
            + "\n\n» ❌ Mesajı sil\n\nİşiniz bittiğinde tekrar deneyin."
        )
        return
    if not a.can_invite_users:
        await m.reply_text(
            "💡 Beni kullanmak için, bana aşağıdaki izni verin:"
            + "\n\n» ❌ Kullanıcı ekleyin\n\nİşiniz bittiğinde tekrar deneyin."
        )
        return
    try:
        ubot = (await user.get_me()).id
        b = await c.get_chat_member(chat_id, ubot)
        if b.status == "kicked":
            await c.unban_chat_member(chat_id, ubot)
            invitelink = await c.export_chat_invite_link(chat_id)
            if invitelink.startswith("https://t.me/+"):
                invitelink = invitelink.replace(
                    "https://t.me/+", "https://t.me/joinchat/"
                )
            await user.join_chat(invitelink)
    except UserNotParticipant:
        try:
            invitelink = await c.export_chat_invite_link(chat_id)
            if invitelink.startswith("https://t.me/+"):
                invitelink = invitelink.replace(
                    "https://t.me/+", "https://t.me/joinchat/"
                )
            await user.join_chat(invitelink)
        except UserAlreadyParticipant:
            pass
        except Exception as e:
            return await m.reply_text(
                f"❌ **userbot katılamadı\n\nneden**: `{e}`"
            )
    if replied:
        if replied.audio or replied.voice:
            suhu = await replied.reply("🤓 **Şarkı Yükleniyor...**")
            dl = await replied.download()
            link = replied.link
            
            try:
                if replied.audio:
                    songname = replied.audio.title[:70]
                    songname = replied.audio.file_name[:70]
                    duration = replied.audio.duration
                elif replied.voice:
                    songname = "Voice Note"
                    duration = replied.voice.duration
            except BaseException:
                songname = "Audio"
            
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                buttons = stream_markup(user_id)
                await suhu.delete()
                await m.reply_photo(
                    photo=f"{IMG_1}",
                    reply_markup=InlineKeyboardMarkup(buttons),
                    caption=f"💡 **Track added to queue »** `{pos}`\n\n🗂 **İsim:** [{songname}]({link}) | `music`\n⏱️ **Zaman:** `{duration}`\n🧸 **İsteyen:** {requester}",
                )
            else:
                try:
                    await suhu.edit("⚡")
                    await call_py.join_group_call(
                        chat_id,
                        AudioPiped(
                            dl,
                        ),
                        stream_type=StreamType().local_stream,
                    )
                    add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                    await suhu.delete()
                    buttons = stream_markup(user_id)
                    requester = (
                        f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                    )
                    await m.reply_photo(
                        photo=f"{IMG_2}",
                        reply_markup=InlineKeyboardMarkup(buttons),
                        caption=f"🗂 **İsim:** [{songname}]({link}) | `music`\n💭 **Gurup:** `{chat_id}`\n🧸 **İsdedi:** {requester}",
                    )
                except Exception as e:
                    await suhu.delete()
                    await m.reply_text(f"🚫 Hata:\n\n» {e}")
        else:
            if len(m.command) < 2:
                await m.reply(
                    "» reply to an **audio file** or **give something to search.**"
                )
            else:
                suhu = await c.send_message(chat_id,"⚡")
                query = m.text.split(None, 1)[1]
                search = ytsearch(query)
                if search == 0:
                    await suhu.edit("❌ **birşey bulunmadı.**")
                else:
                    songname = search[0]
                    title = search[0]
                    url = search[1]
                    duration = search[2]
                    thumbnail = search[3]
                    userid = m.from_user.id
                    gcname = m.chat.title
                    ctitle = await CHAT_TITLE(gcname)
                    image = await thumb(thumbnail, title, userid, ctitle)
                    Akshi, ytlink = await ytdl(url)
                    if Akshi == 0:
                        await suhu.edit(f"❌ yt-dl sorunları algılandı\n\n» `{ytlink}`")
                    else:
                        if chat_id in QUEUE:
                            pos = add_to_queue(
                                chat_id, songname, ytlink, url, "Audio", 0
                            )
                            await suhu.delete()
                            buttons = stream_markup(user_id)
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            await m.reply_photo(
                                photo=image,
                                reply_markup=InlineKeyboardMarkup(buttons),
                                caption=f"💡 **Parça sıraya eklendi »** `{pos}`\n\n🗂 **isim:** [{songname}]({url}) | `music`\n**⏱ Zaman:** `{duration}`\n🧸 **İstedi:** {requester}",
                            )
                        else:
                            try:
                                await suhu.edit("⚡")
                                await call_py.join_group_call(
                                    chat_id,
                                    AudioPiped(
                                        ytlink,
                                        HighQualityAudio(),
                                    ),
                                    stream_type=StreamType().local_stream,
                                )
                                add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                                await suhu.delete()
                                buttons = stream_markup(user_id)
                                requester = (
                                    f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                                )
                                await m.reply_photo(
                                    photo=image,
                                    reply_markup=InlineKeyboardMarkup(buttons),
                                    caption=f"🗂 **İsim:** [{songname}]({url}) | `music`\n**⏱ Zaman:** `{duration}`\n🧸 **İstedi:** {requester}",
                                )
                            except Exception as ep:
                                await suhu.delete()
                                await m.reply_text(f"🚫 hata: `{ep}`")

    else:
        if len(m.command) < 2:
            await m.reply(
                "» bir ses dosyasına yanıt verin veya aranacak bir şey verin."
            )
        else:
            suhu = await c.send_message(chat_id, "⚡")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            if search == 0:
                await suhu.edit("❌ **Şark Bulunmadı.**")
            else:
                songname = search[0]
                title = search[0]
                url = search[1]
                duration = search[2]
                thumbnail = search[3]
                userid = m.from_user.id
                gcname = m.chat.title
                ctitle = await CHAT_TITLE(gcname)
                image = await thumb(thumbnail, title, userid, ctitle)
                Akshi, ytlink = await ytdl(url)
                if Akshi == 0:
                    await suhu.edit(f"❌ yt-dl sorunları algılandı\n\n» `{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                        await suhu.delete()
                        requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                        buttons = stream_markup(user_id)
                        await m.reply_photo(
                            photo=image,
                            reply_markup=InlineKeyboardMarkup(buttons),
                            caption=f"💡 **Parça sıraya eklendi »** `{pos}`\n\n🗂 **İsim:** [{songname}]({url}) | `music`\n**⏱ Zaman:** `{duration}`\n🧸 **İsdedi:** {requester}",
                        )
                    else:
                        try:
                            await suhu.edit("⚡")
                            await call_py.join_group_call(
                                chat_id,
                                AudioPiped(
                                    ytlink,
                                    HighQualityAudio(),
                                ),
                                stream_type=StreamType().local_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                            await suhu.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            buttons = stream_markup(user_id)
                            await m.reply_photo(
                                photo=image,
                                reply_markup=InlineKeyboardMarkup(buttons),
                                caption=f"🗂 **İsim:** [{songname}]({url}) | `music`\n**⏱ Zaman:** `{duration}`\n🧸 **İstedi:** {requester}",
                            )
                        except Exception as ep:
                            await suhu.delete()
                            await m.reply_text(f"🚫 hata: `{ep}`")
