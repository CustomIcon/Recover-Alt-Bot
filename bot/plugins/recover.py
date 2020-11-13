from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from bot import bot
from bot.plugins.helpers import dynamic_data_filter
from bot.plugins.caches import msg_cache
from bot.plugins.clients import pyrogramcli, telethoncli


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
    ses = await client.ask(query.message.chat.id, 'Enter your SessionString for **Telethon**:', reply_markup=ForceReply(True))
    if len(ses.text) < 350:
        await query.message.reply('asumming your SessionString is incorrect! read /start again.')
        return
    try:
        await telethoncli(ses, query=query)
    except Exception as err:
        await query.message.reply(f'**Error:** {err}\n\n try again with /start')


@bot.on_callback_query(dynamic_data_filter("pyrogram_button"))
async def pyrogram_client(client, query):
    await client.delete_messages(
        query.message.chat.id,
        msg_cache[query.from_user.id]
    )
    ses = await client.ask(query.message.chat.id, 'Enter your AUTH_KEY for **Pyrogram**:', reply_markup=ForceReply(True))
    if len(ses.text) < 350:
        await query.message.reply('asumming your AUTH_KEY is incorrect! read /start again.')
        return
    try:
        await pyrogramcli(ses, query=query)
    except Exception as err:
        await query.message.reply(f'**Error:** {err}\n\n try again with /start')