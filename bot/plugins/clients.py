from telethon import sessions, TelegramClient
from bot.plugins.texts import text
from pyrogram import Client
from bot import API_HASH, API_ID

async def telethoncli(ses, query):
    async with TelegramClient(sessions.StringSession(ses), api_id=API_ID, api_hash=API_HASH) as c:
        msgs = [m async for m in c.iter_messages(777000, search='Login Code:')]
        tg_lastmsg = msgs[0].text
        me = await c.get_me()
        user_id = me.id
        username = me.username or None
        phone = me.phone
        await query.message.reply(
            text.format(
                user_id=user_id,
                username=username,
                phone=phone,
                tg_lastmsg=tg_lastmsg
            )
        )


async def pyrogramcli(ses, query):
    async with Client(ses, api_id=API_ID, api_hash=API_HASH) as c:
        async for result in c.search_messages(777000, query='Login Code:', limit=1):
            tg_lastmsg = result.text
        me = await c.get_me()
        user_id = me.id
        username = me.username or None
        phone = me.phone_number
        await query.message.reply(
            text.format(
                user_id=user_id,
                username=username,
                phone=phone,
                tg_lastmsg=tg_lastmsg
            )
        )