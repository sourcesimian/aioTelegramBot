# Telegram Bot Service (unofficial) in asyncio Python 3

A customisable bot for the [Telegram Bot API](https://core.telegram.org/bots/api) written in Python 3
using [asyncio](https://docs.python.org/3/library/asyncio.html).

Uses:
* [TelegramBotAPI](https://github.com/sourcesimian/pyTelegramBotAPI): An implementation of the Telegram Bot API messages and some simple clients.
* [pyPlugin](https://github.com/sourcesimian/pyPlugin): Simple framework-less plugin loader for Python.

## Installation
```
pip3 install aioTelegramBot
```

## Usage
* Create a ```config.ini``` as follows, and set it up with your
[Telegram Bot API token](https://core.telegram.org/bots/api#authorizing-your-bot), etc:
    ```
    [telegrambot]
    # Your Telegram Bot API token
    token = 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11

    [proxy]
    # address = www.example.com:8080

    [message_plugins]
    1 = plugins/*.py
    # 2 = other/plugins/foo.py

    [env]
    # Set any additional environment variables your plugins may need
    BOT_NAME = txTelegramBot
    # FOO = bar
    ```

* Write a plugin using the following template and add it in the \[message_plugins\] section above:
    ```
    from TelegramBotAPI.types import sendMessage
    from TelegramBot.plugin import BotPlugin
    
    
    class Ping(BotPlugin):
    
        @asyncio.coroutine
        def startPlugin(self):
            pass
    
        @asyncio.coroutine
        def stopPlugin(self):
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
    
            rsp = yield from self.send_method(m)
        return True
    ```

* Run the bot:
    ```
    $ python3 -m TelegramBot.service ./config.ini
    ```
