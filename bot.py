import os
import sys
import time
import re
import requests

from telegram.bot import Bot


TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
TELEGRAM_TARGET = os.environ['TELEGRAM_TARGET']
ASANA_TOKEN = os.environ['ASANA_TOKEN']

telegram_bot = Bot(TELEGRAM_TOKEN)


VERBOSE_MODE = os.environ.get('VERBOSE', '0')

if VERBOSE_MODE=='1':
    print("Verbose mode is enabled")

response = requests.get('https://app.asana.com/api/1.0/projects', headers={'Authorization': ASANA_TOKEN})

print(response.json)



#telegram_bot.sendMessage(TELEGRAM_TARGET, msg_string)
