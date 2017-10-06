import os
import sys
import time
import re

from slackclient import SlackClient
from telegram.bot import Bot


def format_slack(s):
        txt_result = s

        m = re.search(r'\<@([a-zA-Z0-9]*?)\>', s)
        if m:
                UID=m.groups()[0]

                user = sc.api_call("users.info",user=UID)['user']
                user_name=user['real_name']

                txt_result = re.sub(r'\<@(.*?)\>', user_name, txt_result)

        # ID: field removal
        txt_result = re.sub(r'(\*ID\:\*\s[0-9]*\n)', '', txt_result)
	# Due date format
        txt_result = re.sub(r'\<\!(date\^.*?\})\|(.*?)\>', r'\2', txt_result)
	# link to project/sub-task format
        txt_result = re.sub(r'\<(https.*?)\|(.*?)\>', r'\2', txt_result)
	# Removing bold formatting
        txt_result = re.sub(r'\*(.*?)\*', r'\1', txt_result)

        return txt_result


SLACK_TOKEN = os.environ['SLACK_TOKEN']
sc = SlackClient(SLACK_TOKEN)

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
TELEGRAM_TARGET = os.environ['TELEGRAM_TARGET']
telegram_bot = Bot(TELEGRAM_TOKEN)

VERBOSE_MODE = os.environ.get('VERBOSE', '0')

if VERBOSE_MODE=='1':
    print("Verbose mode is enabled")

if sc.rtm_connect():
    while True:
        messages = sc.rtm_read()
        for message in messages:
            try:
                if message['type'] == 'message':
                    if VERBOSE_MODE=='1':
                        print(message)
                    if (message['subtype'] == 'bot_message') and (message['bot_id'] == 'B7AMC8MPE'):
                        msg_string = ""
                        for attachement in message['attachments']:
                                text = format_slack(attachement['text'])
                                msg_string += "%s: %s (%s)" % (attachement['fallback'],text,attachement['title_link'])

                    telegram_bot.sendMessage(TELEGRAM_TARGET, msg_string)
            except:
                print('Could not send message.')
                print("Unexpected error:", sys.exc_info()[0])
        time.sleep(1)
else:
    print("Connection Failed, invalid token?")
