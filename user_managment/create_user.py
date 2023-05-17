from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import aiogram.utils.markdown as fmt

from config import dp, bot, URL_WEB_APP, admin_usertag
from keyboards import keys
import db
from text_config.texts import step_2

class Making_user(StatesGroup):
	waiting_for_user_name = State()
	waiting_for_user_stack = State()
	waiting_for_user_id = State()

@dp.message_handler(text='Регистрация🔐', state="*")
async def muser(message: types.Message):
		print(db.if_exists_create(message.chat.id))
		if db.if_exists_create(message.chat.id):
			await bot.send_message(message.chat.id,  f'Ты не можешь создать аккаунт с данного устройства, его id, уже есть в БД.\nВспомни пароль или свяжись с администратором - {admin_usertag}', parse_mode=types.ParseMode.HTML)
		else:
			await bot.send_message(message.chat.id,  f'Привет {message.from_user.first_name} \nВведите Ваш Никнейм, он будет виден пользователям и в вашей группе', parse_mode=types.ParseMode.HTML)
			await Making_user.waiting_for_user_name.set()



@dp.message_handler(state=Making_user.waiting_for_user_name, content_types=types.ContentTypes.TEXT)
async def user_name(message: types.Message, state: FSMContext): 
	await state.update_data(user_name=message.text)
	await Making_user.next()
	mes = await bot.send_message(message.chat.id, f"{message.text.capitalize()},\n"+step_2, reply_markup=keys.skip())
	await state.update_data(mes=mes)


@dp.message_handler(state=Making_user.waiting_for_user_stack, content_types=types.ContentTypes.TEXT)
async def user_stack(message: types.Message, state: FSMContext):
	if "text" in message:
		await state.update_data(stack=message.text)
	else:
		await state.update_data(stack=None)
	user_data = await state.get_data()

	mes = await bot.send_message(user_data['mes'].chat.id, f"{user_data['user_name']}  - Ваш Никнейм\nCоздать профиль?", reply_markup=keys.step_2())
	await state.update_data(mes=mes)
	await Making_user.next()


#INLINE_CALLBACK_PART
@dp.callback_query_handler(lambda c: c.data == 'skip', state = Making_user.waiting_for_user_stack)
async def cancel_handler(message: types.Message, state: FSMContext):
	user_data = await state.get_data()
	await bot.delete_message(user_data['mes'].chat.id, user_data['mes'].message_id)
	await user_stack(message, state)


@dp.callback_query_handler(lambda c: c.data == 'yes_create', state=Making_user.waiting_for_user_id)
async def cancel_handler(message: types.Message, state: FSMContext):
	user_data = await state.get_data()

	db.create_user(user_data['mes']['chat']['id'], user_data['user_name'], user_data['stack'])
	await bot.delete_message(user_data['mes']['chat']['id'], user_data['mes'].message_id)
	await bot.send_message(user_data['mes'].chat.id, 'Поздравляю, вы создали нового пользователя', reply_markup=keys.key_main_menu(), disable_web_page_preview=True)
	await state.finish()

@dp.callback_query_handler(lambda c: c.data == 'cancel', state = Making_user.waiting_for_user_id)
async def cancel_handler(message: types.Message, state: FSMContext):
	user_data = await state.get_data()
	await bot.delete_message(user_data['mes']['chat']['id'], user_data['mes'].message_id)
	await state.finish()