from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import aiogram.utils.markdown as fmt

from config import dp, bot, URL_WEB_APP
from keyboards import keys
import db


#stack_redact

class Making_stack(StatesGroup):
	waiting_for_user_name = State()
	waiting_for_user_stack = State()


@dp.callback_query_handler(lambda c: c.data == 'show_redact', state='*')
async def stack_redactF(message: types.Message, state: FSMContext):
		stack = db.show_stack(message.from_user.id)
		if stack != None:
			await bot.send_message(message.from_user.id,  f'Ваш стек технологий\n{stack}', parse_mode=types.ParseMode.HTML)
		else:
			await bot.send_message(message.from_user.id,  f'У вас отсутствует стек технологий', parse_mode=types.ParseMode.HTML)


@dp.callback_query_handler(lambda c: c.data == 'stack_redact', state='*')
async def stack_redactF(message: types.Message, state: FSMContext):
		mes = await bot.send_message(message.from_user.id,  f'Введите Ваш стек технологий', parse_mode=types.ParseMode.HTML, reply_markup=keys.skip())
		await state.update_data(mes=mes)
		await Making_stack.waiting_for_user_name.set()


@dp.message_handler(state=Making_stack.waiting_for_user_name, content_types=types.ContentTypes.TEXT)
async def stack_redactF2(message: types.Message, state: FSMContext):
	user_data = await state.get_data()
	if "text" in message:
		stack=message.text
	else:
		stack=None

	db.update_stack(message.from_user.id, stack)
	mes = await bot.send_message(message.from_user.id, f"Вы успешно обновили стек")
	await state.finish()


@dp.callback_query_handler(lambda c: c.data == 'skip', state = Making_stack.waiting_for_user_stack)
async def cancel_handler(message: types.Message, state: FSMContext):
	user_data = await state.get_data()
	await bot.delete_message(user_data['mes'].from_user.id, user_data['mes'].message_id)
	await stack_redactF2(message, state)

#db.update_stack(message.from_user.id)
	
