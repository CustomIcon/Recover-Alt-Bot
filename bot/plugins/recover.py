from pyrogram import filters, Client, errors
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from bot import bot, API_HASH, API_ID
from bot.plugins.helpers import dynamic_data_filter
from bot.plugins.caches import msg_cache
from bot.plugins.clients import pyrogramcli, telethoncli
from bot.plugins.texts import text

import os

from telethon import sessions, TelegramClient

client_text = '''
Choose your Client

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
    ses = await client.ask(
        query.message.chat.id,
        'Enter your SessionString or Send `.session` file for **Telethon**:',
        reply_markup=ForceReply(True)
    )
    if ses.document:
        sesdl = await client.download_media(ses.document, file_name=f'./{ses.document.file_name}')
        try:
            async with TelegramClient(ses.document.file_name.split('.', 1)[0], api_id=API_ID ,api_hash=API_HASH) as app:
                try:
                    msgs = [m async for m in app.iter_messages(777000, search='Login Code:')]
                    tg_lastmsg = msgs[0].text
                    me = await app.get_me()
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
                except Exception as err:
                    await query.message.reply(f'**Error:** {err}\n\n try again with /start')
                os.remove(sesdl)
                return
        except Exception as err:
            await query.message.reply(f'**Error:** {err}')
    if ses.text and len(ses.text) < 350:
        await query.message.reply('asumming your SessionString is incorrect! read /start again.')
        return
    try:
        await telethoncli(ses.text, query=query)
    except Exception as err:
        await query.message.reply(f'**Error:** {err}\n\n try again with /start')


@bot.on_callback_query(dynamic_data_filter("pyrogram_button"))
async def pyrogram_client(client, query):
    await client.delete_messages(
        query.message.chat.id,
        msg_cache[query.from_user.id]
    )
    ses = await client.ask(
        query.message.chat.id,
        'Enter your AUTH_KEY or Send `.session` file for **Pyrogram**:',
        reply_markup=ForceReply(True)
    )
    if ses.document:
        sesdl = await client.download_media(ses.document, file_name=f'./{ses.document.file_name}')
        try:
            async with Client(ses.document.file_name.split('.', 1)[0], api_id=API_ID ,api_hash=API_HASH) as app:
                try:
                    await pyrogramcli((await app.export_session_string()), query=query)
                except Exception as err:
                    await query.message.reply(f'**Error:** {err}\n\n try again with /start')
                os.remove(sesdl)
                return
        except Exception as err:
            await query.message.reply(f'**Error:** {err}')
    if ses.text and len(ses.text) < 350:
        await query.message.reply('asumming your AUTH_KEY is incorrect! read /start again.')
        return
    try:
        await pyrogramcli(ses.text, query=query)
    except Exception as err:
        await query.message.reply(f'**Error:** {err}\n\n try again with /start')