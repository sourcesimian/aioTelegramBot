import asyncio


class BotPlugin(object):
    priority = 100

    def __init__(self, cb_send_method):
        self.__cb_send_method = cb_send_method

    @asyncio.coroutine
    def startPlugin(self):
        pass

    @asyncio.coroutine
    def stopPlugin(self):
        pass

    @asyncio.coroutine
    def on_message(self, msg):
        pass

    @asyncio.coroutine
    def send_method(self, method):
        result = yield from self.__cb_send_method(method)
        return result
