from pyrogram import Client, filters
from pyrogram.types import Message
from lunabot import LunaBot, types


api = LunaBot()
# 臨時測試
# api.user = types.User(id='',
#                      email='',
#                      token='',
#                       plan_id='PREMIUM-ONEQTR',
#                      plan_sub_status_='',
#                      plan_expired_at_=,
#                      created_at_=,
#                      updated_at_=)


@Client.on_message(filters.command('ask'))
async def ask(client: Client, message: Message):
    resp = await message.reply_text('_')
    await api.send_message(resp, message.command[1])