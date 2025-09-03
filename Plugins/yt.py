import os, time
from pyrogram import *
from pyrogram import filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery 
from pyrogram.enums import ChatMemberStatus 
from yt_dlp import YoutubeDL
from dragonxxdlib import *
from youtube_search import YoutubeSearch as Y88F8
import requests
import yt_dlp
from asSQL import Client as cl
from .is_admin import owner, admin, add_msg

# =========================
# جلب instance اسمها app من مشروعك
# (يحاول عدة احتمالات شائعة: main.py / loader.py / yamenthon.py / bot.py)
# لا يغيّر أي أمر في الكود—فقط تهيئة ليعمل كبلجن.
# =========================
app = None
_try_targets = [
    ("main", "app"),
    ("main", "bot"),
    ("loader", "app"),
    ("loader", "bot"),
    ("yamenthon", "app"),
    ("yamenthon", "bot"),
    ("bot", "app"),
    ("bot", "bot"),
]
for _mod, _attr in _try_targets:
    try:
        _m = __import__(_mod, fromlist=[_attr])
        app = getattr(_m, _attr)
        if app:
            break
    except Exception:
        pass

if app is None:
    raise RuntimeError("لم أستطع العثور على Client instance باسم app/‏bot داخل مشروعك. \
تأكد أن لديك متغيراً عالمياً app أو bot في أحد الملفات: main.py / loader.py / yamenthon.py / bot.py وقم بتحميل البلجن بعد إنشاء العميل.")

data = cl("protect")
db = data['data']

def stm(seconds: int):
    return '{:02}:{:02}:{:02}'.format(seconds // 3600, seconds % 3600 // 60, seconds % 60)

disable = []

@Client.on_message(filters.command("يوت", ["&",""]), group=20)
async def yttt(app, message):
    if message.text:
        if db.key_exists(f'group_{message.chat.id}') == 1:
            pass
        else:
            return
    if db.get(f"lock_yt_{message.chat.id}"):
        await message.reply(f"⇜ عزيزي {message.from_user.mention} البحث مقفول او معطلة .")
    else:
        if len(message.text.split(None, 1)) < 2:
            return
        query  = message.text.split(None, 1)[1]
        re_ = Y88F8(query, max_results=1).to_dict()
        vid = None
        title = None
        channel = None
        try:
            info = re_[0]
            vid = info['id']
            title = info['title']
            channel = info['channel']
        except Exception as e:
            print(e)
            return await message.reply("⇜ صار خطأ ")
        url = f'https://youtu.be/{vid}'
        ydl_ops = {"format": "bestaudio[ext=m4a]"}
        with yt_dlp.YoutubeDL(ydl_ops) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            if int(info_dict['duration']) > 2605:
                return await message.reply("**⚠️ حد التحميل نص ساعه فقط**")
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        try:
            await message.reply_audio(
                audio=audio_file,
                performer=channel,
                title=title,
                duration=info_dict['duration'],
                caption=f"@YamenThon ~ {stm(info_dict['duration'])}"
            )
        finally:
            if os.path.exists(audio_file):
                try:
                    os.remove(audio_file)
                except Exception:
                    pass

@Client.on_message(filters.command("بحث", ["&",""]), group=20)
async def search(app, message):
    if message.text:
        if db.key_exists(f'group_{message.chat.id}') == 1:
            pass
        else:
            return
    if db.get(f"lock_yt_{message.chat.id}"):
        await message.reply(f"⇜ عزيزي {message.from_user.mention} البحث مقفول او معطلة .")
    else:
        if len(message.text.split(None, 1)) < 2:
            return 
        user_id = message.from_user.id
        query = message.text.split(None, 1)[1]
        re_ = Y88F8(query, max_results=4).to_dict()
        buttons = []
        for r in re_:
            buttons.append(
                [
                    InlineKeyboardButton(
                        r["title"],
                        callback_data=f"{user_id}GET{r['id']}"
                    )
                ]
            )
        await message.reply(
            f"**⤶ هذي نتائج بحثك عن {query} :**",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons)
        )

@Client.on_message(filters.regex("^تعطيل اليوتيوب$|^تعطيل التحميل$") & filters.group, group=21)
async def dis_yt(app, message):
    e = "**⇜ اليوتيوب معطل من قبل .**"
    d = "**⇜ من 「 {} 」 \n⇜ ابشر قفلت اليوتيوب \n༄**"
    
    if message.text:
        if db.key_exists(f'group_{message.chat.id}') == 1:
            pass
        else:
            return
    if owner(message.from_user.id, message.chat.id) or admin(message.from_user.id, message.chat.id):
        if db.get(f'lock_yt_{message.chat.id}') == True:
            await message.reply(e)
        else:
            db.set(f'lock_yt_{message.chat.id}', True)
            await message.reply(d.format(message.from_user.mention))

@Client.on_message(filters.regex("^تفعيل اليوتيوب$|^تفعيل التحميل$") & filters.group, group=22)
async def ena_yt(app, message):
    e = "**⇜ اليوتيوب مفعل من قبل .**"
    d = "**⇜ من 「 {} 」 \n⇜ ابشر فعلت اليوتيوب \n༄**"
    
    if message.text:
        if db.key_exists(f'group_{message.chat.id}') == 1:
            pass
        else:
            return
    if owner(message.from_user.id, message.chat.id) or admin(message.from_user.id, message.chat.id):
        if db.get(f'lock_yt_{message.chat.id}') == False:
            await message.reply(e)
        else:
            db.set(f'lock_yt_{message.chat.id}', False)
            await message.reply(d.format(message.from_user.mention))

@Client.on_callback_query(filters.regex("GET"), group=23)
async def get_info(app, query: CallbackQuery):
    user_id = query.data.split("GET")[0]
    vid_id = query.data.split("GET")[1]
    if not query.from_user.id == int(user_id):
        return await query.answer("⚠️ هذا الأمر لا يخصك ", show_alert=True)
    await query.message.delete()
    yt = Y88F8(f'https://youtu.be/{vid_id}', max_results=1).to_dict()
    title = yt[0]['title']
    url = f'https://youtu.be/{vid_id}'
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("صوت 💿", callback_data=f'{user_id}AUDIO{vid_id}'),
                InlineKeyboardButton("فيديو 🎥", callback_data=f'{user_id}VIDEO{vid_id}'),
            ]
        ]
    )
    await app.send_message(
        query.message.chat.id,
        f"**⤶ العنوان - [{title}]({url})**",
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )

download = InlineKeyboardMarkup(
    [[InlineKeyboardButton("إلين ♪ ", url='t.me/YamenThon')]]
)

upload = InlineKeyboardMarkup(
    [[InlineKeyboardButton("إلين ♪", url='t.me/YamenThon')]]
)

error = InlineKeyboardMarkup(
    [[InlineKeyboardButton("⚠️", url='t.me/YamenThon')]]
)

@Client.on_callback_query(filters.regex("AUDIO"), group=24)
async def get_audii(app, query: CallbackQuery):
    user_id = query.data.split("AUDIO")[0]
    vid_id = query.data.split("AUDIO")[1]
    if not query.from_user.id == int(user_id):
        return await query.answer("⚠️ هذا الأمر لا يخصك ", show_alert=True)
    url = f'https://youtu.be/{vid_id}'
    await query.edit_message_text("**جاري التحميل ..**", reply_markup=download)
    ydl_ops = {"format": "bestaudio[ext=m4a]"}
    with yt_dlp.YoutubeDL(ydl_ops) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        if int(info_dict['duration']) > 3605:
            return await query.edit_message_text("**⚠️ حد التحميل ساعة فقط**", reply_markup=error)
        audio_file = ydl.prepare_filename(info_dict)
        ydl.process_info(info_dict)
    await query.edit_message_text("**جاري الإرسال ..**", reply_markup=upload)
    response = requests.get(info_dict['thumbnail'])
    thumb = f"{vid_id}.png"
    with open(thumb, "wb") as file:
        file.write(response.content)
    user = await app.get_users(int(user_id))
    try:
        await query.message.reply_audio(
            audio_file,
            title=info_dict['title'],
            duration=int(info_dict['duration']),
            performer=info_dict['channel'],
            caption=f'• البحث من -› {user.mention}',
            thumb=thumb  # إذا كنت على Pyrogram v2 ويمكن أن يطلب thumbnail بدل thumb عدّل هنا داخليًا عندك
        )
        doneload = InlineKeyboardMarkup(
            [[InlineKeyboardButton("إلين", url="t.me/YamenThon")]]
        )
        await query.edit_message_text(
            f"** العنوان [{info_dict['title']}]({url})**",
            reply_markup=doneload,
            disable_web_page_preview=True
        )
    finally:
        # تنظيف الملفات
        for _p in (thumb, audio_file):
            if os.path.exists(_p):
                try:
                    os.remove(_p)
                except Exception:
                    pass

@Client.on_callback_query(filters.regex("VIDEO"), group=26)
async def get_video(app, query: CallbackQuery):
    user_id = query.data.split("VIDEO")[0]
    vid_id = query.data.split("VIDEO")[1]
    if not query.from_user.id == int(user_id):
        return await query.answer("⚠️ هذا الأمر لا يخصك ", show_alert=True)
    url = f'https://youtu.be/{vid_id}'
    await query.edit_message_text("**جاري التحميل ..**", reply_markup=download)
    with yt_dlp.YoutubeDL({}) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        if int(info_dict['duration']) > 3605:
            return await query.edit_message_text("**⚠️ حد التحميل ساعة فقط**", reply_markup=error)
    ydl_opts = {
        "format": "best",
        "keepvideo": True,
        "prefer_ffmpeg": False,
        "geo_bypass": True,
        "outtmpl": "%(title)s.%(ext)s",
        "quite": True,
    }
    with YoutubeDL(ydl_opts) as ytdl:
        ytdl_data = ytdl.extract_info(url, download=True)
        file_name = ytdl.prepare_filename(ytdl_data)
    await query.edit_message_text("**جاري الإرسال ..**", reply_markup=upload)
    response = requests.get(info_dict['thumbnail'])
    thumb = f"{vid_id}.png"
    with open(thumb, "wb") as file:
        file.write(response.content)
    user = await app.get_users(int(user_id))
    try:
        await query.message.reply_video(
            file_name,
            duration=int(info_dict['duration']),
            caption=f'• البحث من  -› {user.mention}',
            thumb=thumb  # ملاحظة Pyrogram v2 قد يفضل thumbnail
        )
        doneload = InlineKeyboardMarkup(
            [[InlineKeyboardButton("إلين", url='t.me/YamenThon')]]
        )
        await query.edit_message_text(
            f"**🔗 [{info_dict['title']}]({url})**",
            reply_markup=doneload,
            disable_web_page_preview=True
        )
    finally:
        for _p in (thumb, file_name):
            if os.path.exists(_p):
                try:
                    os.remove(_p)
                except Exception:
                    pass
