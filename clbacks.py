from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import aiogram.utils.markdown as fmt
import asyncio

from config import dp, bot, URL_WEB_APP
from keyboards import keys
import db
import datetime
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
import bot_human
import clbacks
#CALLBACK-FUNCTIONS-----------------------------------
@dp.callback_query_handler(lambda c: 'daily' in c.data, state='*')
async def daylyF(message: types.Message, state: FSMContext):
	end = datetime.datetime.now()
	start = end - datetime.timedelta(days=1)

	responce = await asyncio.to_thread(sasha.get_cve, start, end)
	array_for, array_ids = await asyncio.to_thread(splitter, responce)

	if "daily_file" == message.data:
		doc_path = await asyncio.to_thread(text_to_pdf.gen_pdf, array_for, array_ids) #text_to_pdf.gen_pdf(array_for, array_ids)
		await bot.send_document(chat_id=message.from_user.id, document=open(doc_path,'rb'), caption="Репорт за сегодня")
	else:
		try:
			await bot.send_message(chat_id=message.from_user.id, text='\n'.join(array_ids))
		except aiogram.utils.exceptions.MessageIsTooLong as e:
			print(e)
			message.data = "daily_file"
			await daylyF(message, state)



@dp.callback_query_handler(lambda c: 'weekly' in c.data , state='*')
async def weeklyF(message: types.Message, state: FSMContext):
	end = datetime.datetime.now()
	start = end - datetime.timedelta(days=7)

	responce = await asyncio.to_thread(sasha.get_cve, start, end)
	array_for, array_ids = await asyncio.to_thread(splitter, responce)

	doc_path = await asyncio.to_thread(text_to_pdf.gen_pdf, array_for, array_ids) 
	await bot.send_document(chat_id=message.from_user.id, document=open(doc_path,'rb'), caption="Репорт за неделю")


@dp.callback_query_handler(lambda c: 'monthly' in c.data, state='*')
async def monthlyF(message: types.Message, state: FSMContext):
	end = datetime.datetime.now()
	start = end - datetime.timedelta(days=30)

	responce = await asyncio.to_thread(sasha.get_cve, start, end)
	array_for, array_ids = await asyncio.to_thread(splitter, responce)
	
	doc_path = await asyncio.to_thread(text_to_pdf.gen_pdf, array_for, array_ids) 
	await bot.send_document(chat_id=message.from_user.id, document=open(doc_path,'rb'), caption="Репорт за месяц")

#ON======OFF================================================

@dp.callback_query_handler(lambda c: c.data == 'on', state='*')
async def onF(message: types.Message, state: FSMContext):
	db.update_notif(message.from_user.id, True)
	await message.message.edit_text("🟪Настройки Уведомлений:\nВкл", reply_markup=keys.params(True))

@dp.callback_query_handler(lambda c: c.data == 'off', state='*')
async def offF(message: types.Message, state: FSMContext):
	db.update_notif(message.from_user.id, False)
	await message.message.edit_text("🟪Настройки Уведомлений:\nВыкл", reply_markup=keys.params(False))

@dp.callback_query_handler(lambda c: c.data == 'close', state='*')
async def closeF(message: types.Message, state: FSMContext):
	await bot.delete_message(message.message.chat.id, message.message.message_id)

@dp.callback_query_handler(lambda c: c.data == 'top10h', state='*')
async def top10hF(message: types.Message, state: FSMContext):
	info_cve = main.CveInfo()
	mes = await bot.send_message(chat_id=message.from_user.id, text="🔄Идет обработка вашего запроса")
	ans = await asyncio.to_thread(info_cve.print_daily)
	print(ans)

	answ = await asyncio.to_thread(create_report_short, ans)
	#await bot.send_document(chat_id=message.from_user.id, document=open(file,'rb'))
	await bot.send_message(chat_id=message.from_user.id, text=answ)

@dp.callback_query_handler(lambda c: c.data == 'top10w', state='*')
async def top10wF(message: types.Message, state: FSMContext):
	info_cve = main.CveInfo()
	mes = await bot.send_message(chat_id=message.from_user.id, text="🔄Идет обработка вашего запроса")
	ans = await asyncio.to_thread(info_cve.print_weekly)
	print(ans)

	answ = await asyncio.to_thread(create_report_short, ans)
	#await bot.send_document(chat_id=message.from_user.id, document=open(file,'rb'))
	await bot.send_message(chat_id=message.from_user.id, text=answ)



#CALLBACK--ACCOUNT------------------------------------
@dp.callback_query_handler(lambda c: c.data == 'logout', state='*')
async def logoutF(message: types.Message, state: FSMContext):
	info = db.profile(message.from_user.id)
	db.logout(info[3], message.from_user.id)
	await bot.send_message(chat_id=message.from_user.id, text="Вы вышли из аккаунта", reply_markup=keys.welcome())


@dp.callback_query_handler(lambda c: c.data == 'loginid', state='*')
async def loginidF(message: types.Message, state: FSMContext):
	info = db.profile(message.from_user.id)
	await bot.send_message(chat_id=message.from_user.id, text=f"<tg-spoiler>{info[3]}</tg-spoiler>", parse_mode= 'HTML')


@dp.callback_query_handler(lambda c: c.data == 'generate_qr', state='*')
async def generate_qrF(message: types.Message, state: FSMContext):
	info = db.profile(message.from_user.id)
	img = qrcode.make(info[3])
	name = f"qrcodes/{uuid.uuid4().hex.upper()}.png"
	img.save(name)
	await bot.send_photo(chat_id=message.from_user.id, photo=open(name,'rb'))
			

@dp.message_handler(content_types="web_app_data", state='*')
async def qrcodeF(webAppMes: types.Message, state: FSMContext):
	await state.reset_state()
	code = webAppMes.web_app_data
	ans = db.add_logined(code.data, webAppMes.chat.id)
	if ans:
		info = db.profile_by_code(code.data[:33])
		await bot.send_message(chat_id=webAppMes.chat.id, text=f"Привет, {info[2]}!", reply_markup=keys.key_main_menu(), parse_mode= 'HTML', disable_web_page_preview=True)
	else:
		await bot.send_message(chat_id=webAppMes.chat.id, text=f"QR-CODE не корректный, попробуйте другой", reply_markup=keys.welcome(), parse_mode= 'HTML', disable_web_page_preview=True)
