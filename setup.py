from distutils.core import setup

setup(
    name="aioTelegramBot",
    version="0.1",
    description="TelegramBot Service Framework",
    author="Source Simian",
    author_email='sourcesimian@users.noreply.github.com',
    url='https://github.com/sourcesimian/aioTelegramBot',
    download_url="https://github.com/sourcesimian/aioTelegramBot/tarball/v0.1",
    license='MIT',
    packages=['TelegramBot'],
    install_requires=['python-dateutil',
                      'TelegramBotAPI==0.3.1',
                      'pyPlugin==0.1.2',
                      'aiohttp'
                      ],
    entry_points={
        "console_scripts": [
            "telegrambot=TelegramBot.service:main",
        ]
    },
)
