import psycopg2
import uuid
import hashlib

from config import database, database_user, host, port, pass_db

conn = psycopg2.connect(database=database, user=database_user, password=pass_db, host=host, port=port)
conn.autocommit = True

def create_database_tables_startup(cursor):
	cursor.execute('''CREATE TABLE IF NOT EXISTS tg_users(
					 id SERIAL PRIMARY KEY NOT NULL,
					 telegram_id varchar(32) NOT NULL,
					 name varchar(45) NOT NULL,
					 auth_token varchar(150) NOT NULL,
					 stack varchar(32),
					 notifications BOOLEAN,
					 rating varchar(32),
					 contacts varchar(32)

	)''')
	cursor.execute('''CREATE TABLE IF NOT EXISTS tg_login(
					 id SERIAL PRIMARY KEY NOT NULL,
					 auth_token varchar(32) NOT NULL,
					 telegram_id varchar(32) NOT NULL,
					 telegram_id_logined varchar(32) NOT NULL

	)''')

	return True

def if_exists_create(telegram_id):
	cursor = conn.cursor()
	create_database_tables_startup(cursor)
	cursor.execute(f"SELECT telegram_id FROM tg_users")
	telegram_ids = [list[0] for list in cursor.fetchall()]
	if str(telegram_id) in telegram_ids:
		return True
	else:
		return False


def if_exists(telegram_id):
	cursor = conn.cursor()
	create_database_tables_startup(cursor)
	cursor.execute(f"SELECT telegram_id_logined FROM tg_login")
	telegram_ids = [list[0] for list in cursor.fetchall()]
	if str(telegram_id) in telegram_ids:
		return True
	else:
		return False

def profile(telegram_id):
	cursor = conn.cursor()
	create_database_tables_startup(cursor)
	cursor.execute(f"SELECT auth_token FROM tg_login WHERE telegram_id_logined = \'{telegram_id}\'")
	info = cursor.fetchone()
	print(info[0])
	cursor.execute(f"SELECT * FROM tg_users WHERE auth_token = \'{info[0]}\'")
	info = cursor.fetchone()
	return info

def profile_by_code(code):
	cursor = conn.cursor()
	create_database_tables_startup(cursor)
	cursor.execute(f"SELECT * FROM tg_users WHERE auth_token = \'{code}\'")
	info = cursor.fetchone()
	return info

def add_logined(code, telegram_id_logined):
	cursor = conn.cursor()
	create_database_tables_startup(cursor)
	telegram_id = profile_by_code(code)
	if telegram_id != None:
		telegram_id = telegram_id[1]
		cursor.execute(f"INSERT INTO tg_login(auth_token, telegram_id, telegram_id_logined) VALUES(%s, %s, %s)", (code, telegram_id, telegram_id_logined))
		return True
	else:
		return False

def all_ids():
	cursor = conn.cursor()
	create_database_tables_startup(cursor)
	cursor.execute(f"SELECT telegram_id_logined FROM tg_login")
	telegram_ids_logined = [list[0] for list in cursor.fetchall()]

	cursor.execute(f"SELECT telegram_id, notifications FROM tg_users")
	telegram_ids = cursor.fetchall()
	kostil_blya_ne_pony_kak_cdelat_sql_zaprosom = []
	for u in telegram_ids:
		if str(u[0]) in telegram_ids_logined:
			kostil_blya_ne_pony_kak_cdelat_sql_zaprosom.append(u)
		else:
			pass

	return kostil_blya_ne_pony_kak_cdelat_sql_zaprosom

def logout(code, telegram_id_login):
	cursor = conn.cursor()
	create_database_tables_startup(cursor)
	cursor.execute(f"DELETE FROM tg_login WHERE auth_token = \'{code}\' AND telegram_id_logined = \'{telegram_id_login}\'")
	return True

def create_user(telegram_id, name, stack):
	auth_token = uuid.uuid4().hex.upper()
	print(auth_token)

	rating = 0
	notifications = True

	cursor = conn.cursor()
	create_database_tables_startup(cursor)
	cursor.execute(f"SELECT telegram_id FROM tg_users")

	telegram_ids = [list[0] for list in cursor.fetchall()]
	print(telegram_ids)
	print(telegram_id in telegram_ids)
	if telegram_id in telegram_ids:
		return False, 'Такой пользователь уже сушествует'
	else:
		print(telegram_id, name, auth_token, stack, True, 0, None)
		cursor.execute(f"INSERT INTO tg_users(telegram_id, name, auth_token, stack, notifications, rating, contacts) VALUES(%s, %s, %s, %s, %s, %s, %s)", (telegram_id, name, auth_token, stack, True, 0, None))
		add_logined(auth_token, telegram_id)
		return True, f'Пользователь создан'

#======================================
def show_stack(telegram_id):
	info = profile(telegram_id)
	print(info)

	cursor = conn.cursor()
	create_database_tables_startup(cursor)

	cursor.execute(f"SELECT stack FROM tg_users WHERE auth_token = \'{info[3]}\'")
	info = cursor.fetchone()[0]
	return info


def update_notif(telegram_id, notif):
	info = profile(telegram_id)
	print(info)

	cursor = conn.cursor()
	create_database_tables_startup(cursor)
	if notif:
		cursor.execute(f"UPDATE tg_users SET notifications = True WHERE auth_token = \'{info[3]}\'")
	else:
		cursor.execute(f"UPDATE tg_users SET notifications = False WHERE auth_token = \'{info[3]}\'")
	return True


def update_stack(telegram_id, stack):
	info = profile(telegram_id)
	print(info)

	cursor = conn.cursor()
	create_database_tables_startup(cursor)
	cursor.execute(f"UPDATE tg_users SET stack = \'{stack}\' WHERE auth_token = \'{info[3]}\'")
	return True

