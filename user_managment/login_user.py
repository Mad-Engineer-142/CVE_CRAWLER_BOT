from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import aiogram.utils.markdown as fmt

from config import dp, bot, URL_WEB_APP
from keyboards import keys
import db

class Login_user(StatesGroup):
	waiting_for_user_login_id = State()



@dp.message_handler(text="Логин по токену🔓", state='*')
async def muser(message: types.Message):
		await bot.send_message(message.chat.id,  f'Привет {message.from_user.first_name}\nВведите Ваш Login Id', parse_mode=types.ParseMode.HTML)
		await Login_user.waiting_for_user_login_id.set()


@dp.message_handler(state=Login_user.waiting_for_user_login_id, content_types=types.ContentTypes.TEXT)
async def login_idF(message: types.Message, state: FSMContext): 
	code = message.text[:33]
	ans = db.add_logined(code, message.chat.id)
	if ans:
		info = db.profile_by_code(code)
		print(info)
		await bot.send_message(chat_id=message.chat.id, text=f"Привет, {info[2]}!", reply_markup=keys.key_main_menu(), parse_mode= 'HTML', disable_web_page_preview=True)
		await state.finish()
	else:
		await bot.send_message(chat_id=message.chat.id, text=f"Login Id не корректный, попробуйте другой", reply_markup=keys.welcome(), parse_mode= 'HTML', disable_web_page_preview=True)
