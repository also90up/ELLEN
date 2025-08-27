from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton as Button, InlineKeyboardMarkup as Markup
from kvsqlite.sync import Client as KV
import random, string

# قاعدة بيانات للهمس
db = KV('hms.db', 'hms')
hms = {}

# دالة توليد كود عشوائي
def randCode():
    char = string.ascii_letters + string.digits
    return ''.join(random.choice(char) for _ in range(7))

# 📌 التفعيل بالرد على شخص في المجموعة
@Client.on_message(filters.reply & filters.regex(r"^(اهمس|همسه)$") & filters.group)
async def hamsa_group(c: Client, m: Message):
    chatID = m.chat.id
    fromID = m.from_user.id
    toID = m.reply_to_message.from_user.id
    msgID = m.reply_to_message.id

    if fromID == toID:
        return await m.reply("ميصير تهمس لنفسك", True)
    elif m.reply_to_message.from_user.is_bot:
        return await m.reply("ميصير تهمس لبوت", True)

    code = randCode()
    global hms
    hms = {code: {"chat": chatID, "from": fromID, "to": toID, "id": msgID}}

    keb = [[Button("اضغط هنا", url=f"https://t.me/{c.me.username}?start={code}")]]
    await m.reply(
        f"⇜ تم تحديد الهمسه لـ {m.reply_to_message.from_user.mention}\n⇜ اضغط الزر لكتابة الهمسة\n✓",
        True,
        reply_markup=Markup(keb)
    )

# 📌 المستخدم المرسل يكتب الهمسه في الخاص
@Client.on_message(filters.regex(r"^/start\s[a-zA-Z0-9]{7}$") & filters.private)
async def hamsa_private(c: Client, m: Message):
    code = m.text.split(" ")[1]
    userID = m.from_user.id
    global hms

    if hms.get(code):
        chatID = hms[code]["chat"]
        fromID = hms[code]["from"]
        toID = hms[code]["to"]
        toIN = await c.get_users(toID)
        msgID = hms[code]["id"]
        code2 = randCode()

        if userID == fromID:
            ask = await m.chat.ask(
                "⇜ ارسـل همسـة الميـديـا الان \n"
                "تستطيـع الهمـس بجميـع انـواع الميديـا \n"
                "⇜ نص - صورة - ملصق - متحركة - فيديو - صوت \n"
                "⇜ تستطيـع ايضاً ارسـال الميديـا بكابشـن",
                filters=filters.user(fromID),
                reply_to_message_id=m.id
            )

            if ask.text:
                hms[code].update({"type": 1, "msg": ask.text})
                keb = [[Button("افتح الهمسه", callback_data=f"open_{code}")],
                       [Button(f"اهمس ل {m.from_user.first_name}", url=f"https://t.me/{c.me.username}?start={code2}")]]
            elif ask.photo:
                hms[code].update({"type": 2, "msg": getattr(ask, "caption"), "fileID": ask.photo.file_id})
                keb = [[Button("افتح الهمسه", url=f"https://t.me/{c.me.username}?start=open_{code}")],
                       [Button(f"اهمس ل {m.from_user.first_name}", url=f"https://t.me/{c.me.username}?start={code2}")]]
            elif ask.sticker:
                hms[code].update({"type": 3, "msg": getattr(ask, "caption"), "fileID": ask.sticker.file_id})
                keb = [[Button("افتح الهمسه", url=f"https://t.me/{c.me.username}?start=open_{code}")],
                       [Button(f"اهمس ل {m.from_user.first_name}", url=f"https://t.me/{c.me.username}?start={code2}")]]
            elif ask.animation:
                hms[code].update({"type": 4, "msg": getattr(ask, "caption"), "fileID": ask.animation.file_id})
                keb = [[Button("افتح الهمسه", url=f"https://t.me/{c.me.username}?start=open_{code}")],
                       [Button(f"اهمس ل {m.from_user.first_name}", url=f"https://t.me/{c.me.username}?start={code2}")]]
            elif ask.video:
                hms[code].update({"type": 5, "msg": getattr(ask, "caption"), "fileID": ask.video.file_id})
                keb = [[Button("افتح الهمسه", url=f"https://t.me/{c.me.username}?start=open_{code}")],
                       [Button(f"اهمس ل {m.from_user.first_name}", url=f"https://t.me/{c.me.username}?start={code2}")]]
            elif ask.voice:
                hms[code].update({"type": 6, "msg": getattr(ask, "caption"), "fileID": ask.voice.file_id})
                keb = [[Button("افتح الهمسه", url=f"https://t.me/{c.me.username}?start=open_{code}")],
                       [Button(f"اهمس ل {m.from_user.first_name}", url=f"https://t.me/{c.me.username}?start={code2}")]]
            else:
                return await m.reply("ماعرفت نوع الرسالة 🚫")

            txt = f"⇜ عمࢪي 「 {toIN.mention} 」\n⇜ لديك همسة سرية من「 {m.from_user.mention} 」"
            await m.reply("⇜ تم ارسـال الهمسـة .. بنجـاح", True)

            msg = await c.send_message(
                chatID,
                txt,
                reply_to_message_id=msgID,
                reply_markup=Markup(keb)
            )

            db.set(code, hms[code])
            hms = {code2: {"chat": chatID, "from": toID, "to": fromID, "id": msg.id}}
        else:
            await m.reply("انقلع الامر ليس لك", True)

# 📌 فتح الهمسه (ميديا)
@Client.on_message(filters.regex(r"^/start\sopen_[a-zA-Z0-9]{7}$") & filters.private)
async def open_hamsa(c: Client, m: Message):
    code = m.text.split("_")[1]
    if db.exists(code):
        data = db.get(code)
        type = data["type"]
        if m.from_user.id in [data["to"], data["from"]]:
            if type == 2:
                await m.reply_photo(data["fileID"], caption=data["msg"], quote=True)
            elif type == 3:
                await m.reply_sticker(data["fileID"], quote=True)
            elif type == 4:
                await m.reply_animation(data["fileID"], caption=data["msg"], quote=True)
            elif type == 5:
                await m.reply_video(data["fileID"], caption=data["msg"], quote=True)
            elif type == 6:
                await m.reply_voice(data["fileID"], caption=data["msg"], quote=True)
        else:
            await m.reply("انقلع الهمسه مو لك", True)

# 📌 فتح الهمسه (نصوص من الزر)
@Client.on_callback_query(filters.regex(r"^open_[a-zA-Z0-9]{7}$"))
async def open_hamsa_cb(c: Client, m: CallbackQuery):
    code = m.data.split("_")[1]
    if db.exists(code):
        data = db.get(code)
        if m.from_user.id in [data["to"], data["from"]]:
            await m.answer(data["msg"], True)
        else:
            await m.answer("انقلع الهمسه مو لك", True)
