import os
import json
from dotenv import load_dotenv
from pyrogram import Client

from src.utils.print_t import print_t
from src.utils.random import random_from_array

load_dotenv()

# https://my.telegram.org/
TELEGRAM_API_ID = os.getenv('TELEGRAM_API_ID')
TELEGRAM_API_HASH = os.getenv('TELEGRAM_API_HASH')

# @JsonDumpBot ('message' -> 'forward_from_chat' -> 'id')
CHANNELS = list(map(int, json.loads(os.getenv('CHANNELS'))))
USERS = list(map(int, json.loads(os.getenv('USERS'))))

REACTIONS = json.loads(os.getenv('REACTIONS'))

client = Client(
    'react_spammer',
    api_id=TELEGRAM_API_ID,
    api_hash=TELEGRAM_API_HASH
    )


@client.on_message()
async def handler(_, message):
    message_id = message.message_id
    chat = getattr(message, 'chat', None)
    from_user = getattr(message, 'from_user', None)

    chat_id = getattr(chat, 'id', None)
    chat_title = getattr(chat, 'title', None)

    from_user_id = getattr(from_user, 'id', None)
    from_username = getattr(from_user, 'username', None)

    try:
        if (chat_id not in CHANNELS):
            return

        if (from_user_id not in USERS):
            return

        random_react = random_from_array(REACTIONS)

        await client.send_reaction(message_id=message_id, chat_id=chat_id, emoji=random_react)

        print_t(f'chat: {chat_title}({chat_id}) | from: {from_username}({from_user_id}) - reacted by {random_react}')

    except Exception as error:
        print_t(f'chat: {chat_title}({chat_id}) | from: {from_username}({from_user_id}).\nError {error}')


def start():
    print_t('react spammer started')
    client.run()
