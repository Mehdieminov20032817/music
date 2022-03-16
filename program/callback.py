from driver.queues import QUEUE
from pyrogram import Client, filters
from program.utils.inline import menu_markup
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from config import (
    ASSISTANT_NAME,
    BOT_NAME,
    BOT_USERNAME,
    GROUP_SUPPORT,
    OWNER_NAME,
    UPDATES_CHANNEL,
)


@Client.on_callback_query(filters.regex("cbstart"))
async def cbstart(_, query: CallbackQuery):
    await query.answer("home start")
    await query.edit_message_text(
        f"""✨ **Hoş geldin [{query.message.chat.first_name}](tg://user?id={query.message.chat.id}) !**\n
💭 **[{BOT_NAME}](https://t.me/{BOT_USERNAME}) yeni Telegram'ın görüntülü sohbetleri aracılığıyla gruplarda müzik ve video oynatmanıza olanak tanır!**
💡 **» 📚 Komutlar düğmesini tıklayarak Bot'un tüm komutlarını ve nasıl çalıştıklarını öğrenin!**
🔖 **Bu botun nasıl kullanılacağını öğrenmek için lütfen » ❓ Temel Kılavuz düğmesine tıklayın!**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "➕ Beni Grubuna ekle ➕",
                        url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                    )
                ],
                [InlineKeyboardButton("❓ Temel Kılavuz", callback_data="cbhowtouse")],
                [
                    InlineKeyboardButton("📚 Komutlar", callback_data="cbcmds"),
                    InlineKeyboardButton("👨🏻‍💻 Creator", url=f"https://t.me/{OWNER_NAME}"),
                ],
                [
                    InlineKeyboardButton(
                        "💭 Sohbet Grup", url=f"https://t.me/{GROUP_SUPPORT}"
                    ),
                    InlineKeyboardButton(
                        "🎧 Music Kanal", url=f"https://t.me/{UPDATES_CHANNEL}"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "🌐 Support", url="https://t.me/GalaxyCrime"
                    )
                ],
            ]
        ),
        disable_web_page_preview=True,
    )


@Client.on_callback_query(filters.regex("cbhowtouse"))
async def cbguides(_, query: CallbackQuery):
    await query.answer("user guide")
    await query.edit_message_text(
        f"""❓ Bu Bot nasıl kullanılır?, aşağıdaki Gui'yi okuyun!
1.) Öncelikle bu botu Grubunuza ekleyin.
2.) Bu botu Grupta yönetici olarak tanıtın, ayrıca Anonim yönetici dışındaki tüm izinleri verin.
3.) Bu botu tanıttıktan sonra, yönetici verilerini güncellemek için Grup'a /reload yazın.
3.) Grubunuza @{ASSISTANT_NAME} ekleyin veya onu eklemek için /userbotjoin yazın (maalesef /play (şarkı adı) veya /vplay (şarkı adı) yazarken userbot kendisine katılacak).
4.) Viyo/müzik çalmaya başlamadan önce viyo sohbetini açın/başlatın.
- SON, HER ŞEY AYARLANDI -
📌 Userbot vio sohbete katılmadıysa, vio sohbetin zaten açık olduğundan ve userbot'un sohbette olduğundan emin olun.
💡 Bu bot hakkında takip eden bir sorunuz varsa, buradaki destek sohbetimde söyleyebilirsiniz:@{GROUP_SUPPORT}.""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Geri dön", callback_data="cbstart")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbcmds"))
async def cbcmds(_, query: CallbackQuery):
    await query.answer("commands menu")
    await query.edit_message_text(
        f"""✨ **Selam [{query.message.chat.first_name}](tg://user?id={query.message.chat.id}) !**
» Açıklamayı okumak ve mevcut Komutların listesini görmek için aşağıdaki menüyü seçin !
⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("👷🏻 Admin Komutları", callback_data="cbadmin"),
                    InlineKeyboardButton("🧙🏻 Sudo Konutları", callback_data="cbsudo"),
                ],[
                    InlineKeyboardButton("📚 Normal Konutlar", callback_data="cbbasic")
                ],[
                    InlineKeyboardButton("🔙 Geri dön", callback_data="cbstart")
                ],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("cbbasic"))
async def cbbasic(_, query: CallbackQuery):
    await query.answer("basic commands")
    await query.edit_message_text(
        f"""🏮 işte temel komutlar:
» /play (şarkı adı/bağlantı) - video sohbette müzik çal
» /vplay (video adı/bağlantı) - video sohbette vio oyna
» /vstream - canlı video om yt live/mp3 oyna
» /playlist - size çalma listesini gösterir
» /vio (song) - youtube'dan vio indir
» /song (song) - youtube üzerinden şarkı indir
» /lyric (song) - şarkı sözlerini not edin
» /search (song) - youtube vio bağlantısını arayın
» /ping - botun ping durumunu göster
» /uime - bot kullanıcı arayüzü durumunu göster
» /alive - show the bot alive info (in Group only)
⚡️ __Powered by {BOT_NAME} AI__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Geri dön", callback_data="cbcmds")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbadmin"))
async def cbadmin(_, query: CallbackQuery):
    await query.answer("admin commands")
    await query.edit_message_text(
        f"""🏮 işte yönetici komutları:
» /pause - akışı duraklat
» /rume - akışı rume
» /atla - sonraki akışa geç
» /stop - akışı durdur
» /vmute - sesli sohbette kullanıcı robotunu sessize alır
» /vunmute - sesli sohbette kullanıcı robotunun sesini açar
» /volume 1-200 - müziğin sesini ayarlayın (userbot yönetici olmalıdır)
» /reload - botu yeniden yükleyin ve yönetici verilerini yeniden yükleyin
» /userbotjoin - gruba katılmak için userbot'u dahil edin
» /userbotleave - veya userbot om grubundan ayrılır
⚡️ __Powered by {BOT_NAME} AI__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Geri dön", callback_data="cbcmds")]]
        ),
    )

@Client.on_callback_query(filters.regex("cbsudo"))
async def cbsudo(_, query: CallbackQuery):
    await query.answer("sudo commands")
    await query.edit_message_text(
        f"""🏮 işte sudo komutları:
» /gban (kullanıcı adı veya kullanıcı kimliği) - küresel olarak yasaklanmış kişiler için
» /ungban (kullanıcı adı veya kullanıcı kimliği) - küresel olmayan yasaklı kişiler için
» /speedtt - bot sunucusu speedtt'i çalıştırın
» /sysinfo - sistem bilgilerini göster
» /update - botunuzu latt sürümüne güncelleyin
» /rtart - botunuzu yeniden başlatın
» /leaveall - veya userbot tüm gruptan ayrılır
» /leavebot (sohbet kimliği) - veya belirttiğiniz gruptan ayrılmak için bot
» /eval - herhangi bir işbirliğini yürütür
» /sh - herhangi bir komutu çalıştır
» /broadcast (mesaj) - bot tarafından taranan tüm gruplara bir yayın mesajı gönderir
» /broadcast_pin (mesaj) - sohbet pininden her ikisi tarafından da aranan tüm gruplara bir yayın mesajı gönderir
⚡ __Powered by {BOT_NAME} AI__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Geri dön", callback_data="cbcmds")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbmenu"))
async def cbmenu(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 Yalnızca bu düğmeye dokunabilen görüntülü sohbet yönetme iznine sahip yönetici !", show_alert=True)
    chat_id = query.message.chat.id
    user_id = query.message.from_user.id
    buttons = menu_markup(user_id)
    chat = query.message.chat.title
    if chat_id in QUEUE:
          await query.edit_message_text(
              f"⚙️ **Settings of** {chat}\n\n⏸ : akışı duraklat\n▶️ : rume akışını durdur\n🔇 : userbot'un sesini kapat\n🔊 : userbot'un sesini aç\n⏹ : akışı durdur",
              reply_markup=InlineKeyboardMarkup(buttons),
          )
    else:
        await query.answer("❌ şu anda hiçbir şey yayınlanmıyor", show_alert=True)


@Client.on_callback_query(filters.regex("cls"))
async def close(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 Yalnızca bu düğmeye dokunabilen görüntülü sohbet yönetme iznine sahip yönetici !", show_alert=True)
    await query.message.delete()
