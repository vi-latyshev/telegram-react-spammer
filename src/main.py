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
# array '["", ""]'
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
    chat_id = message.chat.id
    from_user_id = getattr(getattr(message, 'from_user', None), 'id', None)

    try:
        if (chat_id not in CHANNELS):
            return

        if (from_user_id not in USERS):
            return

        random_react = random_from_array(REACTIONS)

        await client.send_reaction(message_id=message_id, chat_id=chat_id, emoji=random_react)

        print_t(f'message (chat_id id: {chat_id}) (from_id {from_user_id}) reacted by {random_react}')

    except Exception as error:
        print_t(f'error react message (chat_id: {chat_id}) (from_id {from_user_id}). Error {error}')


def start():
    print_t('forwarder started')
    client.run()
