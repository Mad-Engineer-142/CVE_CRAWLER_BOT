from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import aiogram.utils.markdown as fmt

from q import dp, bot
from keyboards import keys
import db
import asyncio


from text_config.texts import *
from cve_managment import main, chat_gpt, github_parser

#top10

#@dp.message_handler(is_logged=True, state='*')
async def cve_search_id(message: types.Message):
	mes = await bot.send_message(chat_id=message.chat.id, text="🔄Идет обработка вашего запроса")
	#CVE nist
	info_cve = main.CveInfo()
	print('WATSAAAAAAAAAAAAAAAAAAAOOOOOOOOOO!1111111111')
	ans, for_gpt = await asyncio.to_thread(info_cve.print_by_id, message.text)
	print('WATSAAAAAAAAAAAAAAAAAAAOOOOOOOOOO!222222222')
	if for_gpt != None:
		print('WATSAAAAAAAAAAAAAAAAAAAOOOOOOOOOO!333333333')
		github_data = await asyncio.to_thread(github_parser.get_by_id, ans[0][2:])


		awsa =  await asyncio.to_thread(chat_gpt.chatgpt_req, ans[0], ans[8])

		answ, name = await asyncio.to_thread(create_report, ans, awsa, github_data)

		await bot.delete_message(mes.chat.id, mes.message_id)
		#await bot.send_document(chat_id=message.from_user.id, document=open(name,'rb'), caption="\n".join(res_text[:3]))
		await bot.send_message(chat_id=message.chat.id, text=answ,  disable_web_page_preview=True)
	else:
		await bot.delete_message(mes.chat.id, mes.message_id)
		#await bot.send_document(chat_id=message.from_user.id, document=open(name,'rb'), caption="\n".join(res_text[:3]))
		await bot.send_message(chat_id=message.chat.id, text=ans,  disable_web_page_preview=True)