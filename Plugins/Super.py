import random, re, time, pytz
from datetime import datetime
from threading import Thread
from pyrogram import *
from pyrogram.enums import *
from pyrogram.types import *
from config import *
from helpers.Ranks import *
from helpers.Ranks import isLockCommand
from pyrogram import Client, filters
from pyrogram.types import ChatMemberUpdated, Message
from datetime import datetime
import pytz

default_welcome = """أهلاً وسهلاً 💐
الاسم: {الاسم}
المعرف: {اليوزر}
المجموعة: {المجموعه}
التاريخ: {التاريخ}
الوقت: {الوقت}
"""

@Client.on_chat_member_updated()
async def welcome_new_member(c: Client, m: ChatMemberUpdated):
    # نتأكد انه عضو جديد انضم
    if m.new_chat_member.status == "member":
        user = m.new_chat_member.user
        chat = m.chat

        # معلومات العضو
        name = user.first_name
        username = f"@{user.username}" if user.username else "بدون معرف"
        title = chat.title

        # الوقت والتاريخ
        TIME_ZONE = "Asia/Riyadh"
        ZONE = pytz.timezone(TIME_ZONE)
        TIME = datetime.now(ZONE)
        clock = TIME.strftime("%I:%M %p")
        date = TIME.strftime("%d/%m/%Y")

        # نص الترحيب
        welcome = default_welcome.replace("{الاسم}", name)\
                                 .replace("{اليوزر}", username)\
                                 .replace("{المجموعه}", title)\
                                 .replace("{الوقت}", clock)\
                                 .replace("{التاريخ}", date)

        # ارسال الترحيب
        try:
            await c.send_message(chat.id, welcome)
        except Exception as e:
            print("خطأ عند إرسال الترحيب:", e)
