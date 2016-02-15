import asyncio

from TelegramBotAPI.types import sendMessage, sendPhoto
from TelegramBotAPI.types import Message

from TelegramBot.plugin import BotPlugin

from datetime import datetime

import logging

log = logging.getLogger(__name__)


class Timer(BotPlugin):
    priority = 10
    _user_ids = None

    @asyncio.coroutine
    def startPlugin(self):
        self._user_ids = {}

    @asyncio.coroutine
    def stopPlugin(self):
        pass

    @asyncio.coroutine
    def on_tick(self, chat_id):
        log.info('Sending time to %s' % chat_id)
        m = sendMessage()
        m.chat_id = chat_id
        m.text = "Time now is: %s" % datetime.now()
        yield from self.send_method(m)

    @asyncio.coroutine
    def ticker(self, chat_id, period):
        while True:
            yield from self.on_tick(chat_id)
            yield from asyncio.sleep(period)

    @asyncio.coroutine
    def on_message(self, msg):
        if not hasattr(msg, 'text'):
            return False

        if msg.text.lower() == 'timer start':
            log.info('Timer started for %s' % msg.chat.id)

            loop = asyncio.get_event_loop()
            self._user_ids[msg.chat.id] = loop.create_task(self.ticker(msg.chat.id, 5))

            m = sendMessage()
            m.chat_id = msg.chat.id
            self._chat_id = msg.chat.id
            m.text = 'Timer started'
            yield from self.send_method(m)
            return True

        if msg.text.lower() == 'timer stop':
            log.info('Timer started for %s' % msg.chat.id)

            if msg.chat.id in self._user_ids:
                self._user_ids[msg.chat.id].cancel()
                del self._user_ids[msg.chat.id]

            m = sendMessage()
            m.chat_id = msg.chat.id
            m.text = 'Timer stopped'
            yield from self.send_method(m)
            return True
