# This script uses BeautifulSoup4 to access the HTML source code of the website, and checking its value with
# the source code 5 seconds ago. If the two match, the website hasn't changed. If they don't, the website has
# changed and the user is alerted using Telegram immediately.

import requests
from bs4 import BeautifulSoup as soup
import hashlib
from datetime import timedelta
from datetime import datetime

from telegram.ext import Updater, CommandHandler
import re

updater = Updater(token=API_TOKEN, use_context=True)  # Replace with your API_TOKEN
dispatcher = updater.dispatcher
j = updater.job_queue
data = requests.get(
    'https://jeemain.nta.nic.in/webinfo/public/home.aspx',
    headers={'User-Agent': 'Mozilla/5.0'}
).content

sp = soup(data, features='html.parser')
out_str = sp.text
groups = []
with open('groups.dat') as f:
    for line in f.readlines():
        if line.strip() != '':
            groups.append(int(line))


def everytime(context):
    global out_str
    data = requests.get('https://jeemain.nta.nic.in/webinfo/public/home.aspx',
                        headers={'User-Agent': 'Mozilla/5.0'}).content
    sp = soup(data, features='html.parser')
    new_str = sp.text
    count = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape('Result'), new_str))
    if new_str != out_str:
        for my_id in groups:
            context.bot.send_message(chat_id=my_id, text='Website changed!!' + new_str)
        out_str = new_str
    else:
        print('Not changed!!')


def start(update, context):
    new_id = update.effective_chat.id
    if new_id in groups:
        context.bot.send_message(chat_id=update.effective_chat.id, text='I am running!')
    else:
        groups.append(new_id)
        with open('groups.dat', 'a') as f:
            f.write(str(new_id))
            f.write('\n')
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Task completed successfullyi. I\'ll inform you whenever the website changes. To view if I\'m running, type /start'
        )


def latest(update, context):
    data = requests.get('https://jeemain.nta.nic.in/webinfo/public/home.aspx',
                        headers={'User-Agent': 'Mozilla/5.0'}).content
    sp = soup(data, features='html.parser')
    tags = sp.find_all('li')[3].text
    context.bot.send_message(chat_id=update.effective_chat.id, text=tags)


# Replace 5 with the interval you want to check the website for changes
j.run_repeating(everytime, interval=timedelta(seconds=5), first=datetime.utcnow()+timedelta(seconds=2))
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('latest', latest))
updater.start_polling()
updater.idle()
