from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from bot import bot, API_HASH, API_ID
from bot.plugins.helpers import dynamic_data_filter
from bot.plugins.caches import msg_cache

from telethon import sessions, TelegramClient

from bot.plugins.texts import text

client_text = '''
Choose the your client

**Note:** You cannot use Telethon string inside the pyrogram client,
it is totally different. Same rules are applied for Pyrogram.
'''

@bot.on_callback_query(dynamic_data_filter("accept_button"))
async def create(client, query):
    msg_cache[query.from_user.id] = query.message.message_id
    buttons = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton(
                'Telethon', callback_data='telethon_button'
            ),
            InlineKeyboardButton(
                'Pyrogram', callback_data='pyrogram_button'
            )
        ]]
    )
    await query.message.edit(client_text, reply_markup=buttons)
    await query.answer()


@bot.on_callback_query(dynamic_data_filter("telethon_button"))
async def telethon_client(client, query):
    await client.delete_messages(
        query.message.chat.id,
        msg_cache[query.from_user.id]
    )
    ses = await client.ask(query.message.chat.id, 'Enter your SessionString for telthon:', reply_markup=ForceReply(True))
    async with TelegramClient(sessions.StringSession(ses.text), api_id=API_ID, api_hash=API_HASH) as c:
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


@bot.on_callback_query(dynamic_data_filter("pyrogram_button"))
async def pyrogram_client(client, query):
    await client.delete_messages(
        query.message.chat.id,
        msg_cache[query.from_user.id]
    )
    ses = await client.ask(query.message.chat.id, 'Enter your AUTH_KEY for pyrogram:', reply_markup=ForceReply(True))
    async with Client(ses.text, api_id=API_ID, api_hash=API_HASH) as c:
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