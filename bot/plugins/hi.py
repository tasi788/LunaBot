from pyrogram import Client, filters


@Client.on_message(filters.command('hi'))
async def hi(_, message):
    await message.reply_text('Hello world')