from aiogram import types
from aiogram.types.web_app_data import WebAppData
from config import URL_WEB_APP, URL_WEB_APP_PARAMS

def web_app(url):
	#inline_btn_1 = types.ReplyKeyboardMarkup(resize_keyboard=False).add(types.KeyboardButton(text="🔐Получить доступ коду🔐"))
	inline_btn_2 = types.ReplyKeyboardMarkup(resize_keyboard=False).add(types.KeyboardButton(text="🌎Получить доступ по сайту🌎",  web_app=WebAppData(url=url)))
	return inline_btn_2

def key_main_menu():
	markup5 = types.ReplyKeyboardMarkup().row()
	markup5.row(types.KeyboardButton("🔥Начать"), types.KeyboardButton("📊Профиль"))
	markup5.row(types.KeyboardButton('😎О Боте', web_app=WebAppData(url=URL_WEB_APP)), types.KeyboardButton('⚙️Параметры⚙'))
	return markup5



def skip():
	inline_btn_5 = types.InlineKeyboardButton('Пропустить⤵️', callback_data='skip')
	inline_kb1 = types.InlineKeyboardMarkup().add(inline_btn_5)
	return inline_kb1

def step_2():
	inline_btn_5 = types.InlineKeyboardMarkup()
	inline_btn_5.add(types.InlineKeyboardButton(text='Да', callback_data='yes_create'))
	inline_btn_5.add(types.InlineKeyboardButton(text='Отмена', callback_data='cancel'))
	return inline_btn_5

def generate_qr():
	inline_btn_5 = types.InlineKeyboardMarkup()
	inline_btn_5.add(types.InlineKeyboardButton(text='Сгенерировать QR?', callback_data='generate_qr'))
	inline_btn_5.add(types.InlineKeyboardButton(text='Скопировать Login Id', callback_data='loginid'))
	inline_btn_5.add(types.InlineKeyboardButton(text='🛑Выйти из аккаунта🛑', callback_data='logout'))
	inline_btn_5.add(types.InlineKeyboardButton(text='❎Закрыть', callback_data='close'))
	return inline_btn_5


def begin():
	inline_btn_5 = types.InlineKeyboardMarkup()
	inline_btn_5.add(types.InlineKeyboardButton(text="Топ 10 cve на данный момент", callback_data='top10'))
	inline_btn_5.add(types.InlineKeyboardButton(text='Самые свежие за неделю', callback_data='fresh'))
	return inline_btn_5
#✅❌
def params(notif):
	inline_btn_5 = types.InlineKeyboardMarkup()
	#inline_btn_5.add(types.InlineKeyboardButton(text='Посмотреть Стек', callback_data='show_redact'))
	#inline_btn_5.add(types.InlineKeyboardButton(text='Редактировать Стек', callback_data='stack_redact'))
	if notif:
		inline_btn_5.add(types.InlineKeyboardButton(text='☑️ВКЛ', callback_data='on'), types.InlineKeyboardButton(text='ВЫКЛ', callback_data='off'))
	else:
		inline_btn_5.add(types.InlineKeyboardButton(text='ВКЛ', callback_data='on'), types.InlineKeyboardButton(text='☑️ВЫКЛ', callback_data='off'))
	inline_btn_5.add(types.InlineKeyboardButton(text='❎Закрыть', callback_data='close'))
	return inline_btn_5

#📝🧧
def main_func():
	inline_btn_5 = types.InlineKeyboardMarkup()
	inline_btn_5.add(types.InlineKeyboardButton(text='📝За дату', callback_data='date'))
	inline_btn_5.add(types.InlineKeyboardButton(text='📝За день', callback_data='daily'), types.InlineKeyboardButton(text='🧧За день', callback_data='daily_file'))
	inline_btn_5.add(types.InlineKeyboardButton(text='🧧За неделю', callback_data='weekly'), types.InlineKeyboardButton(text='🧧За за месяц', callback_data='monthly'))
	inline_btn_5.add(types.InlineKeyboardButton(text="🧧Топ 10 cve на данный момент за 24ч", callback_data='top10h'))
	inline_btn_5.add(types.InlineKeyboardButton(text="🧧Топ 10 cve на данный момент за 7 дней", callback_data='top10w'))
	inline_btn_5.add(types.InlineKeyboardButton(text='❎Закрыть', callback_data='close'))
	return inline_btn_5


def generate_scroll(func, position, max_pos):
	inline_btn_5 = types.InlineKeyboardMarkup()
	if position == 0:
		inline_btn_5.add(types.InlineKeyboardButton(text='>', callback_data=f'{func}_>'))
	elif position == max_pos:
		inline_btn_5.add(types.InlineKeyboardButton(text='<', callback_data=f'{func}_<'))
	else:
		inline_btn_5.add(types.InlineKeyboardButton(text='>', callback_data=f'{func}_>'))
		inline_btn_5.add(types.InlineKeyboardButton(text='<', callback_data=f'{func}_<'))
	return inline_btn_5

def welcome():
	markup5 = types.ReplyKeyboardMarkup().row()
	markup5.row(types.KeyboardButton("Логин по QR-Коду🔓", web_app=WebAppData(url=URL_WEB_APP_PARAMS)), types.KeyboardButton("Логин по токену🔓"))
	markup5.row(types.KeyboardButton("Регистрация🔐"))
	return markup5

