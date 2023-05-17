import os
import sys
import time

from telethon.sync import TelegramClient, events
from telethon.sessions import StringSession
from config import API_ID, API_HASH, SESSION_STRING

from telethon.sync import TelegramClient


def send_messages(message, users):
	for user in users:
		client.send_message(user, message)
		print(f"Message sent to {user}.")


def start():
	client = TelegramClient(SESSION_STRING, API_ID, API_HASH)
	client.start()
	@client.on(events.NewMessage(chats = ''))
	async def main(event):
		me = await client.get_me()
		print(event)
		print(event.peer_id.user_id)
		if event.peer_id.user_id==:
			await client.send_message('', event.message)
		else:
			pass

	return True
	client.run_until_disconnected()