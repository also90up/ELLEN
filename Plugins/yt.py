# Plugins/yt.py
import os
import requests
import threading
import yt_dlp
from pyrogram import *
from pyrogram.enums import *
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from youtube_search import YoutubeSearch as YTSearch
from config import *   # يجلب المتغيرات العامة مثل r, botUsername, hmshelp

def stm(seconds):
    return '{:02}:{:02}:{:02}'.format(seconds // 3600, seconds % 3600 // 60, seconds % 60)

# أمر التحميل السريع: &يوت <كلمة البحث>
@Client.on_message(filters.command("يوت", ["&",""]) & filters.group, group=20)
def yttt(c, m):
    if len(m.text.split(None, 1)) < 2:
        return
    query = m.text.split(None, 1)[1]
    try:
        res = YTSearch(query, max_results=1).to_dict()
        info = res[0]
        vid = info['id']
        title = info.get('title', 'Unknown')
        channel = info.get('channel', '')
    except Exception as e:
        print("YT search error:", e)
        return m.reply("⇜ صار خطأ في البحث")
    url = f'https://www.youtube.com/watch?v={vid}'

    def download_and_send():
        ydl_opts = {
            "format": "bestaudio[ext=m4a]",
            "outtmpl": f"{vid}.%(ext)s",
            "noplaylist": True,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                duration = int(info_dict.get('duration') or 0)
                if duration > 1800:  # 30 دقيقة حد افتراضي
                    return m.reply("**⚠️ حد التحميل: 30 دقيقة فقط**")
                # download
                ydl.download([url])
                ext = info_dict.get('ext') or 'm4a'
                audio_file = f"{vid}.{ext}"
                # thumbnail
                thumb = None
                try:
                    thumb_url = info_dict.get('thumbnail')
                    if thumb_url:
                        rr = requests.get(thumb_url, timeout=15)
                        with open(f"{vid}.jpg", "wb") as f:
                            f.write(rr.content)
                        thumb = f"{vid}.jpg"
                except:
                    thumb = None
                try:
                    m.reply_audio(audio=audio_file,
                                  performer=channel,
                                  title=title,
                                  duration=duration,
                                  caption=f"@{botUsername} ~ {stm(duration)}",
                                  thumb=thumb)
                except Exception as e:
                    m.reply(f"حدث خطأ أثناء الإرسال: {e}")
                finally:
                    try: os.remove(audio_file)
                    except: pass
                    if thumb:
                        try: os.remove(thumb)
                        except: pass
        except Exception as e:
            print("yt_dlp error:", e)
            try: m.reply("حدث خطأ أثناء التحميل.")
            except: pass

    threading.Thread(target=download_and_send).start()

# أمر البحث: &بحث <كلمة>
@Client.on_message(filters.command("بحث", ["&",""]) & filters.group, group=21)
def search(c, m):
    if len(m.text.split(None, 1)) < 2:
        return
    query = m.text.split(None, 1)[1]
    try:
        results = YTSearch(query, max_results=4).to_dict()
    except Exception as e:
        print("search err", e)
        return m.reply("⇜ صار خطأ في البحث")
    buttons = []
    user_id = m.from_user.id
    for r in results:
        title = (r.get("title") or "")[:60]
        buttons.append([InlineKeyboardButton(title, callback_data=f"{user_id}GET{r['id']}")])
    m.reply(f"**⤶ هذي نتائج بحثك عن {query} :**", disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons))

# المستخدم يضغط على نتيجة -> نعرض له خيارات صوت/فيديو
@Client.on_callback_query(filters.regex(r"^\d+GET") , group=22)
def get_info(c, query: CallbackQuery):
    data = query.data
    user_id = data.split("GET")[0]
    vid_id = data.split("GET")[1]
    if query.from_user.id != int(user_id):
        return query.answer("⚠️ هذا الأمر لا يخصك", show_alert=True)
    try:
        query.message.delete()
    except:
        pass
    try:
        yt = YTSearch(f'https://youtu.be/{vid_id}', max_results=1).to_dict()
        title = yt[0]['title']
    except:
        title = vid_id
    url = f'https://youtu.be/{vid_id}'
    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton("صوت 💿", callback_data=f'{user_id}AUDIO{vid_id}'),
          InlineKeyboardButton("فيديو 🎥", callback_data=f'{user_id}VIDEO{vid_id}')]]
    )
    c.send_message(query.message.chat.id, f"**⤶ العنوان - [{title}]({url})**",
                   disable_web_page_preview=True, reply_markup=reply_markup)

# تحميل الصوت بعد الضغط
@Client.on_callback_query(filters.regex(r"AUDIO") , group=23)
def get_audio(c, query: CallbackQuery):
    data = query.data
    user_id = data.split("AUDIO")[0]
    vid_id = data.split("AUDIO")[1]
    if query.from_user.id != int(user_id):
        return query.answer("⚠️ هذا الأمر لا يخصك ", show_alert=True)
    url = f'https://youtu.be/{vid_id}'
    try:
        query.edit_message_text("**جاري التحميل ..**")
    except:
        pass
    ydl_opts = {"format": "bestaudio[ext=m4a]", "outtmpl": f"{vid_id}.%(ext)s", "noplaylist": True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            duration = int(info_dict.get('duration') or 0)
            if duration > 3600:
                return query.edit_message_text("**⚠️ حد التحميل ساعة فقط**")
            ydl.download([url])
            ext = info_dict.get('ext') or 'm4a'
            audio_file = f"{vid_id}.{ext}"
        # thumbnail
        thumb = None
        try:
            thumb_url = info_dict.get('thumbnail')
            if thumb_url:
                rr = requests.get(thumb_url, timeout=15)
                with open(f"{vid_id}.jpg", "wb") as f:
                    f.write(rr.content)
                thumb = f"{vid_id}.jpg"
        except:
            thumb = None
        user = c.get_users(int(user_id))
        query.message.reply_audio(audio_file,
                                 title=info_dict.get('title'),
                                 duration=duration,
                                 performer=info_dict.get('uploader', ''),
                                 caption=f'• البحث من -› {user.mention}',
                                 thumb=thumb)
        query.edit_message_text(f"** العنوان [{info_dict.get('title')}]({url})**", disable_web_page_preview=True)
    except Exception as e:
        print("audio err", e)
        try: query.edit_message_text("حدث خطأ أثناء التحميل")
        except: pass
    finally:
        try: os.remove(f"{vid_id}.jpg")
        except: pass
        try: os.remove(audio_file)
        except: pass

# تحميل الفيديو بعد الضغط
@Client.on_callback_query(filters.regex(r"VIDEO") , group=24)
def get_video(c, query: CallbackQuery):
    data = query.data
    user_id = data.split("VIDEO")[0]
    vid_id = data.split("VIDEO")[1]
    if query.from_user.id != int(user_id):
        return query.answer("⚠️ هذا الأمر لا يخصك ", show_alert=True)
    url = f'https://youtu.be/{vid_id}'
    try:
        query.edit_message_text("**جاري التحميل ..**")
    except:
        pass
    try:
        with yt_dlp.YoutubeDL({"format": "best", "outtmpl": f"{vid_id}.%(ext)s", "noplaylist": True}) as ytdl:
            info_dict = ytdl.extract_info(url, download=False)
            duration = int(info_dict.get('duration') or 0)
            if duration > 3600:
                return query.edit_message_text("**⚠️ حد التحميل ساعة فقط**")
            ytdl.download([url])
            # find downloaded file name (may be different ext)
            # here we expect: vid_id.ext
            file_name = f"{vid_id}.{info_dict.get('ext') or 'mp4'}"
        # thumbnail
        thumb = None
        try:
            thumb_url = info_dict.get('thumbnail')
            if thumb_url:
                rr = requests.get(thumb_url, timeout=15)
                with open(f"{vid_id}.jpg", "wb") as f:
                    f.write(rr.content)
                thumb = f"{vid_id}.jpg"
        except:
            thumb = None
        user = c.get_users(int(user_id))
        query.message.reply_video(file_name, duration=duration, caption=f'• البحث من -› {user.mention}', thumb=thumb)
        query.edit_message_text(f"**🔗 [{info_dict.get('title')}]({url})**", disable_web_page_preview=True)
    except Exception as e:
        print("video err", e)
        try: query.edit_message_text("حدث خطأ أثناء التحميل")
        except: pass
    finally:
        try: os.remove(f"{vid_id}.jpg")
        except: pass
        try: os.remove(file_name)
        except: pass
