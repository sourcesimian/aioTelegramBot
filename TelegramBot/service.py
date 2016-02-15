#!/usr/bin/env python

import asyncio
import logging
import os

from configparser import ConfigParser
import argparse

from pyplugin import PluginLoader

from TelegramBotAPI.client.asyncioclient import AsyncioClient
from TelegramBotAPI.types.methods import getUpdates

from TelegramBot.logger import basic_logging
from TelegramBot.plugin import BotPlugin

basic_logging()
log = logging.getLogger(__name__)


class TelegramBotService(object):

    def __init__(self, token, plugin_filespec, proxy=None, debug=False):
        self._update_id = 0
        self._client = AsyncioClient(token, proxy=proxy, debug=debug)

        self._plugins = [p(self._send_method) for p in PluginLoader(BotPlugin, plugin_filespec)]

        self._plugins.sort(key=lambda p: p.priority)

    @asyncio.coroutine
    def run(self):
        for plugin in self._plugins:
            yield from plugin.startPlugin()

        try:
            while True:
                method = getUpdates()
                method.offset = self._update_id
                method.timeout = 30
                updates = yield from self._client.send_method(method)

                for update in updates:
                    yield from self._on_update(update)
                    self._update_id = update.update_id + 1
                # if not len(updates):
                #     yield from asyncio.sleep(10)

        except KeyboardInterrupt:
            log.info('Stopping ...')

        for plugin in self._plugins:
            yield from plugin.stopPlugin()

    @asyncio.coroutine
    def _on_update(self, update):
        for plugin in self._plugins:
            handled = yield from plugin.on_message(update.message)
            if handled:
                break

    @asyncio.coroutine
    def _send_method(self, method):
        result = yield from self._client.send_method(method)
        return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('config', help='INI config file')
    args = parser.parse_args()

    config = ConfigParser()
    config.optionxform = str
    config.read(args.config)

    token = config['telegrambot']['token']

    proxy = config['proxy'].get('address', None)
    if proxy:
        os.environ['http_proxy'] = 'http://%s' % proxy
        os.environ['https_proxy'] = 'https://%s' % proxy

    msg_plugins = [v for v in config['message_plugins'].values()]

    for key, value in config['env'].items():
        os.environ[key] = value

    service = TelegramBotService(token, msg_plugins, proxy, debug=True)

    asyncio.get_event_loop().run_until_complete(service.run())


if __name__ == "__main__":
    exit(main())
