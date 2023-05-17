from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor
from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher import FSMContext
from aiogram.utils.web_app import safe_parse_webapp_init_data
from aiohttp.web_request import Request
from aiohttp.web_response import json_response
from aiogram.dispatcher.filters.state import State, StatesGroup

import datetime
import asyncio
import aiogram
from dateutil.parser import parse
import json
import zipfile 

from aiogram.dispatcher import Dispatcher, filters
from filters.customs import logged, from_second

import uuid
import qrcode

from config import dp, bot, URL_WEB_APP
from text_config.texts import *
from user_managment import create_user, login_user, team
from cve_managment import main, chat_gpt
import cve_func
from keyboards import keys
import sasha
import text_to_pdf
import db

import clbacks
import search_sploit


dp.filters_factory.bind(logged)
dp.filters_factory.bind(from_second)

class Getting_info(StatesGroup):
	slider = State()

class Date_parse(StatesGroup):
	begin_parse = State()
	end_parse = State()

#Handlers-----------------------------------------------------------
@dp.message_handler(commands=['start'], state="*")
async def startF(message: types.Message):
	state = dp.current_state(user=message.from_user.id)
	await state.finish()
	if db.if_exists(message.chat.id):
		await bot.send_message(chat_id=message.chat.id, text=f"Привет, {message.from_user.first_name}!", reply_markup=keys.key_main_menu(), disable_web_page_preview=True)
	else:
		await bot.send_message(chat_id=message.chat.id, text=f"Привет, {message.from_user.first_name}\nВыбери что ты хочешь сделать:", reply_markup=keys.welcome(), disable_web_page_preview=True)

@dp.message_handler(is_logged=True, text="🔥Начать", state='*')
async def startF2(message: types.Message, state: FSMContext):
	await state.finish()
	await bot.send_message(chat_id=message.chat.id, text=f"{begin}\nВыберите промежуток времени для вывода CVE:", parse_mode= 'HTML', reply_markup=keys.main_func())

@dp.message_handler(is_logged=True, commands=['profile'], state="*")
async def ProfileF(message: types.Message, state: FSMContext):
	await state.finish()
	info = db.profile(message.chat.id)
	textus = text_generator_profile(info)
	await bot.send_message(chat_id=message.chat.id, text=textus, parse_mode= 'HTML', reply_markup=keys.generate_qr())

@dp.message_handler(is_logged=True, text="📊Профиль", state='*')
async def ProfileF2(message: types.Message, state: FSMContext):
	await state.finish()
	info = db.profile(message.chat.id)
	textus = text_generator_profile(info)
	await bot.send_message(chat_id=message.chat.id, text=textus, parse_mode= 'HTML', reply_markup=keys.generate_qr())


@dp.message_handler(is_logged=True, text="⚙️Параметры⚙", state='*')
async def paramsF(message: types.Message, state: FSMContext):
	await state.finish()
	info = db.profile(message.from_user.id)
	if info[5]:
		await bot.send_message(chat_id=message.chat.id, text="🟪Настройки Уведомлений:\nВкл", parse_mode= 'HTML', reply_markup=keys.params(True))
	else:
		await bot.send_message(chat_id=message.chat.id, text="🟪Настройки Уведомлений:\nВыкл", parse_mode= 'HTML', reply_markup=keys.params(False))
#----------------------------------------------------------------------


#KEYWORD CVE HANLER=====================================================
@dp.message_handler(regexp=r"(CVE+(-[A-Za-z0-9]+)+)")
@dp.message_handler(regexp=r'CVE_[0-9]+_[0-9]+')
@dp.message_handler(filters.RegexpCommandsFilter(regexp_commands=['CVE_[0-9]+_[0-9]+']), state='*')
async def vector(message: types.Message, state: FSMContext):
	if '/' and "_" in message.text:
		message.text = message.text[1:].replace("_", '-')
		print(message.text)
	await cve_func.cve_search_id(message)
#=====================================================================
@dp.callback_query_handler(lambda c: c.data == 'date', state='*')
async def date(message: types.Message, state: FSMContext):
	mes = await bot.send_message(chat_id=message.from_user.id, text="Введите начальный период в формате (YYYY-MM-DD)")
	await Date_parse.begin_parse.set()
	await state.update_data(mes=mes)



@dp.message_handler(state=Date_parse.begin_parse)
async def begin_parseF(message: types.Message, state: FSMContext):
	user_data = await state.get_data()
	if "mes_to_del" in user_data:
		try:
			await bot.delete_message(user_data['mes_to_del'].chat.id, user_data['mes_to_del'].message_id)
		except Exception:
			pass
	try:
		begin_parse = parse(message.text)
		await bot.delete_message(user_data['mes'].chat.id, user_data['mes'].message_id)
		mes = await bot.send_message(chat_id=message.from_user.id, text="Введите конечный период в формате (YYYY-MM-DD)")
		await state.update_data(begin_parse=begin_parse)

	except Exception as e:
		mes_to_del = await bot.send_message(chat_id=message.from_user.id, text="Дата введена неверно!\nВведите начальный период в формате (YYYY-MM-DD)")
		await state.update_data(mes_to_del=mes_to_del)
		return
	await state.update_data(mes=mes)
	await Date_parse.end_parse.set()

@dp.message_handler(state=Date_parse.end_parse)
async def end_parseF(message: types.Message, state: FSMContext):
	user_data = await state.get_data()
	if "mes_to_del" in user_data:
		try:
			await bot.delete_message(user_data['mes_to_del'].chat.id, user_data['mes_to_del'].message_id)
		except Exception:
			pass
	try:
		end_parse = parse(message.text)
		await bot.delete_message(user_data['mes'].chat.id, user_data['mes'].message_id)
		mesdel = await bot.send_message(chat_id=message.from_user.id, text="🔄Идет обработка вашего запроса")

		end = end_parse
		start = user_data['begin_parse']

		if start > end:
			responce = sasha.get_cve(str(end)[:-3], str(start)[:-3])
		elif start < end: 
			responce = sasha.get_cve(str(start)[:-3], str(end)[:-3])
		elif start == end:
			responce = sasha.get_cve(str(start)[:-3], str(end)[:-8]+"23:59")
		if responce != []:
			array_for, array_ids = splitter(responce)

			try:
				await bot.send_message(chat_id=message.from_user.id, text='\n'.join(array_ids))
				await bot.delete_message(mesdel.chat.id, mesdel.message_id)
			except aiogram.utils.exceptions.MessageIsTooLong as e:
				await bot.delete_message(mesdel.chat.id, mesdel.message_id)
				doc_path = await asyncio.to_thread(text_to_pdf.gen_pdf, array_for, array_ids)
				await bot.send_document(chat_id=message.from_user.id, document=open(doc_path,'rb'), caption="Репорт за запрошенные даты")
		else:
			await bot.send_message(chat_id=message.from_user.id, text="По вашим датам ничего не найдено")

	except Exception as e:
		mes_to_del = await bot.send_message(chat_id=message.from_user.id, text="Дата введена неверно!\nВведите конечный период в формате (YYYY-MM-DD)")
		await state.update_data(mes_to_del=mes_to_del)
		return
	await state.finish()

	
@dp.message_handler(state=None)
async def keyword_searchF(message: types.Message, state: FSMContext):
		await state.finish()
		if db.if_exists(message.chat.id):
			mesdel = await bot.send_message(chat_id=message.from_user.id, text="🔄Идет обработка вашего запроса")

			result = search_sploit.search(message.text)
			json_object = json.loads(result)
			print(json_object)
			res_text, res_files = json_parser(json_object)
			if res_text:
				await bot.delete_message(mesdel.chat.id, mesdel.message_id)
				file_buffer = []
				name = f"files/{uuid.uuid4().hex.upper()}.zip"
				print(name)
				with zipfile.ZipFile(name, 'w') as f:
					for u in res_files[:3]:
						f.write(u)
				await bot.send_document(chat_id=message.from_user.id, document=open(name,'rb'), caption="\n".join(res_text[:3]))
			else:
				await bot.delete_message(mesdel.chat.id, mesdel.message_id)
		else:
			pass


#START---POINT---------------------------------------
if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)
