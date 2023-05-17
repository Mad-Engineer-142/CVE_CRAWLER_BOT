from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from user_managment import create_user
import db
from config import dp, bot
from keyboards import keys

class logged(BoundFilter):
	key = 'is_logged'

	def __init__(self, is_logged):
		self.is_logged = is_logged

	async def check(self, message: types.Message):
		print('check')
		if db.if_exists(message.chat.id):
			return True
		else:
			state = dp.current_state(user=message.from_user.id)
			await state.finish()
			if db.if_exists(message.chat.id):
				await bot.send_message(chat_id=message.chat.id, text=f"Привет, {message.from_user.first_name}!", reply_markup=keys.key_main_menu(), disable_web_page_preview=True)
			else:
				await bot.send_message(chat_id=message.chat.id, text=f"Привет, {message.from_user.first_name}\nВыбери что ты хочешь сделать:", reply_markup=keys.welcome(), disable_web_page_preview=True)
			return False

class from_second(BoundFilter):
	key = 'from_second'

	def __init__(self, from_second):
		self.from_second = from_second

	async def check(self, message: types.Message):
		if message.from_user.id == 6002532052 or message.from_user.id == 5695394252:
			return True
		else:
			return False
