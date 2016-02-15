import asyncio
import logging
import os

from TelegramBotAPI.types import sendMessage, sendPhoto

from TelegramBot.plugin import BotPlugin

log = logging.getLogger(__name__)


class Ping(BotPlugin):

    @asyncio.coroutine
    def startPlugin(self):
        pass

    @asyncio.coroutine
    def on_message(self, msg):

        if hasattr(msg, 'text'):
            m = sendMessage()
            m.chat_id = msg.chat.id
            if msg.text == 'Hello':
                m.text = 'Hello my name is %s' % os.environ['BOT_NAME']
            else:
                m.text = 'You said: "%s"' % msg.text
        elif hasattr(msg, 'photo'):
            m = sendPhoto()
            m.chat_id = msg.chat.id
            m.caption = "What a pong!"
            m.photo = msg.photo[0].file_id
        else:
            return False

        rsp = yield from self.send_method(m)
        return True
