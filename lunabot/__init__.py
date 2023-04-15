from typing import Union

import aiohttp
from . import types
import random
from pyrogram.errors import FloodWait, MessageNotModified, UserBlocked
from pyrogram.types import Message
import json


class LunaBot:
    def __init__(self):
        self.url: str = 'https://api.lunabot.ai/api'
        self.session = aiohttp.ClientSession()
        self.user: types.User = None

    async def login(self, email: str) -> bool:
        data = {'email': email}
        async with self.session.post(f'{self.url}/login', json=data) as resp:
            if resp.ok:
                r = await resp.json()
                if r['code'] != 0:
                    raise Exception(r['message'])
                return True
            return False

    async def login_code(self, email: str, code: str) -> Union[types.User, bool]:
        data = {'email': email, 'code': code}
        async with self.session.post(f'{self.url}/login', json=data) as resp:
            if resp.ok:
                r = await resp.json()
                print(r)
                if r['code'] != 0:
                    raise Exception(r['message'])
                self.user = types.User.from_dict(r['data']['user'])
                return self.user
            return False

    async def send_message(self,
                           msg: Message,
                           text: str,
                           model: str = 'gpt3_5'):
        headers = {
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'x-aibot-uuid': '',
            'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
            'x-aibot-version': '1.2.3',
            'dnt': '1',
            'x-aibot-token': self.user.token,
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            'content-type': 'application/json',
            'x-aibot-platform': 'chrome',
            'x-aibot-lang': 'zh-TW',
            'accept': '*/*',
            'origin': 'chrome-extension://jkeolmadidncndcbnajhaojepbolajag',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'sec-gpc': '1',
        }

        json_data = {
            'channelId': '',
            'title': '',
            'url': '',
            'type': 'CHAT',
            'text': text,
            'model': 'gpt3_5',
            'pageContents': [],
            'promptCommands': [],
        }
        async with self.session.post(f'{self.url}/sendMessage', headers=headers, json=json_data) as resp:
            queue_text = ''
            async for line in resp.content:
                context = line.decode('utf8')

                # 隨機回應列隊字串，然後做人要 50% 50%
                # https://youtu.be/d_od1uYJhiM?t=654
                idk = random.randint(1, 100)
                if context.startswith('data:'):
                    queue_text += json.loads(context.split('data:')[1])['text']

                    if idk >= 50:
                        try:
                            await msg.edit_text(queue_text)
                        except MessageNotModified:
                            # telegram 智障日常
                            pass
                        except UserBlocked:
                            # 使用者封鎖我了
                            return

                if context.startswith('event'):
                    try:
                        # 確保列隊文字有全部傳送過去
                        await msg.edit_text(queue_text)
                    except MessageNotModified:
                        pass
                    except UserBlocked:
                        pass
                    return

    async def refresh_token(self):
        # https://api.lunabot.ai/api/refreshToken
        pass
