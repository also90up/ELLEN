import time, redis, os, json, re, requests, asyncio 
from pyrogram import *
from asSQL import Client as cl
r = redis.Redis('localhost',decode_responses=True)

to_config = """
import redis
r = redis.Redis('localhost',decode_responses=True)
"""



print('''
Offices being installed…''')
print('\n\n')

try:
  from information import *
  hmshelp = token.split(':')[0]
  r.set(f'{hmshelp}botowner', owner_id)
except Exception as e:
  with open ('information.py','w+') as www:
     token = input ('[+] Enter the bot token : ')
     hmshelp = token.split(':')[0]
     if not r.get(f'{hmshelp}botowner'):
       owner_id = int(input('[+] Enter SUDO ID : '))
       r.set(f'{hmshelp}botowner', owner_id)
     else:
        owner_id = int(r.get(f'{hmshelp}botowner'))
     text = 'token = "{}"\nowner_id = {}'
     www.write(text.format(token, owner_id))



if not r.get(f'{hmshelp}botowner'):
    owner_id = int(input('[+] Enter SUDO ID : '))
    r.set(f'{hmshelp}botowner', owner_id)
else:
    owner_id = int(r.get(f'{hmshelp}botowner'))
print('''
Database is being created''')

to_config += f"\ntoken = '{token}'"
to_config += f"\nhmshelp = token.split(':')[0]"
to_config += f"\nsudo_id = {owner_id}"
username = requests.get(f"https://api.telegram.org/bot{token}/getMe").json()["result"]["username"]
to_config += f"\nbotUsername = '{username}'"
to_config += "\nfrom kvsqlite.sync import Client as DB"
to_config += "\nytdb = DB('ytdb.sqlite')"
to_config += "\nsounddb = DB('sounddb.sqlite')"
to_config += "\nwsdb = DB('wsdb.sqlite')"

with open('config.py','w+') as w:
  w.write(to_config)
print('''
Database is being sorted''')
app = Client(f'{hmshelp}r3d', 15263491, 'f6cf6c2263f1e933f24d86bf02311467',
  bot_token=token,
    plugins={"root": "Plugins"},
  )
# userbot = Client('userbott', 15263491, "f6cf6c2263f1e933f24d86bf02311467", session_string="BACPaOQAw9EWMijb1D8m_wYGIa2r6tnaNiJDVTuC4jVktrtF5K7UxjNuZNcA-HpmEBltGr-0rUrELER9Vj0CmkNb28BdGYGETl5dJIg386wdjv3ZYNB3HkYrbhN5GFE4w2tYNv5dQJmvLTtvC3bTa0HoW64YLPINX_3BEZSoyXPm_bbXonA_2PIqeA1MHdEzfg_U4Zy75xyBq0pBvTv6xhD9hpAliXHnapJ5gg4C8Qt4QX4JLMGYxaSTNt51OClNVpPU6yiKZBFYl-t6CP66VmL3JU3P3HshrCSlcY38GfZ7Uy_w1b7HCqqe9EnVmZV0k3S29YtFlGz9Z0uuw0pxloAFpebeTwAAAABydGQqAA")
  
if not r.get(f'{hmshelp}:botkey'):
    r.set(f'{hmshelp}:botkey', '⇜')

if not r.get(f'{hmshelp}botname'):
    r.set(f'{hmshelp}botname', 'الين')

if not r.get(f'{hmshelp}botchannel'):
    r.set(f'{hmshelp}botname', 'ELLNEVIP_BOT')

def Find(text):
  m = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s!()\[\]{};:'\".,<>?«»“”‘’]))"
  url = re.findall(m,text)  
  return [x[0] for x in url]
  
# @app.on_message(filters.group & filters.regex("^انستا "), group=-1)
# async def instaDownlo(c,m):
#   if not r.get(f'{m.chat.id}:disableINSTA:{hmshelp}') and Find(m.text):
#     url = Find(m.text)[0]
#     rep = await m.reply("...")
#     await m.reply_chat_action(enums.ChatAction.TYPING)
#     msg = await userbot.send_message("instasavegrambot", url)
#     await rep.edit("Wait ...")
#     await asyncio.sleep(20)
#     await m.reply_chat_action(enums.ChatAction.UPLOAD_DOCUMENT)
#     msg = await userbot.get_messages("instasavegrambot",msg.id+1)
#     await rep.delete()
#     if msg.media_group_id:
#        r.set("media:insta", f"{m.chat.id}&&&{m.id}", ex=10)
#        msg = await userbot.copy_media_group("iwwbot", "instasavegrambot",msg.id)
#     else:
#        msg = await msg.download("./")
#        try:
#           return await m.reply_video(msg)
#        except:
#           pass
#        try:
#           return await m.reply_animation(msg)
#        except:
#           pass
       
#        try:
#           return await m.reply_photo(msg)
#        except:
#           pass
       
#        try:
#           return await m.reply_document(msg)
#        except:
#           pass
#        os.remove(msg)
    
     
# @app.on_message(filters.private & filters.user(1920230442))
# async def mediagCopy(c,m):
#    if r.get("media:insta") and m.media_group_id:
#       chat_id = r.get("media:insta").split("&&&")[0]
#       id = r.get("media:insta").split("&&&")[1]
#       await c.copy_media_group(int(chat_id), m.from_user.id, m.id,reply_to_message_id=int(id))
#       r.delete("media:insta")
      
data = cl("protect")
db = data['data']
db.create_table()

app.start()
# userbot.start()
print('''
🇾🇪 Run Bot Send /Start ''')
if r.get(f'DevGroup:{hmshelp}'):
  id = int(r.get(f'DevGroup:{hmshelp}'))
  try:
    app.send_message(id, "تم اتشغيل البوت بنجاح ✔️")
  except:
    pass
idle()
  
