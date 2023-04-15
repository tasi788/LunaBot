from lunabot import LunaBot,types
import asyncio
from bot import Bot

bot: Bot = Bot()

# async def main():
#     client = LunaBot()
#     await client.send_message('Hello world')

if __name__ == '__main__':
    bot.start_serve()
