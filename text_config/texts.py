import requests
import re
import search_sploit
import json

welcome_text = """
Приветствую! Я бот, который предназначен для предоставления информации о уязвимостях Common Vulnerabilities and Exposures (CVE). Для того, чтобы начать пользоваться моими функциями, Вам необходимо зарегистрироваться."""
step_2 = "введите личный стек используемых технологий (например, Apache, nginx, PHP, MySQL и т.д.), чтобы я мог предоставить Вам информацию о наиболее актуальных уязвимостях."

begin = """
Вы можете ввести определенную CVE  получить развернутую информацию по ней, или нажать на кнопки ниже
Ответ на ваш запрос будет снабжен наиболее полной информацией о CVE, а также более развернутым ответом от ChatGPT
"""
emoji_arr = ['⚛️','🔗','📎','📌','⛔️','🔺','🔻','🤖','👁‍🗨']


def text_generator_profile(info):
	#(2, '1066122447', 'ff', '02DA01F7B3C14FC49D54CD03D20DF8C6', None, True, '0', None)
	if info[5]:
		text = f"🟣Ваш профиль {info[2]}\n\n🟪Login Id: <tg-spoiler>{info[3]}</tg-spoiler>\n🟪Подписан на уведомления: ✅\n🟪Ваш рейтинг: {info[6]}"
	else:
		text = f"🟣Ваш профиль {info[2]}\n\n🟪Login Id: <tg-spoiler>{info[3]}</tg-spoiler>\n🟪Подписан на уведомления: ⛔️\n🟪Ваш рейтинг: {info[6]}"

	if info[7] != None:
		text = text + f"\n🟪Вы состоите в команде: {info[7]}"
	else:
		text = text + f"\n🟪Вы не состоите в команде"

	return text



def change_format(textus):
	print(textus.split('\n'))
	textus_splitted = textus.split('\n')
	if '‼️' in textus_splitted[0]:
		print("!!")
		cve_id = textus_splitted[2].replace('-', "_")
		cve_id = f"/{cve_id}"
		text = textus_splitted[3:]
		text = '\n'.join(text)
		return f"♨️\n{cve_id}\nБез Описания"

	elif textus_splitted[0][0] == '🔔':
		print('🔔')
		cve_id = textus_splitted[0][4:].split("➡️")[0]
		cve_id = cve_id.replace('-', "_")
		cve_id = f"/{cve_id[1:]}"

		desc = textus_splitted[2:-2]
		desc = '\n'.join(desc)
		name   =  textus_splitted[0][5:].split("➡️")[-1]
		return f"♨️\n{textus_splitted[0][3]}\n{cve_id}\n{name}\n{desc}"
		
	elif "📣🌡 ♨" in textus_splitted[0][0:5]:
		print("123")

		cve_id = textus_splitted[0][7:].split("➡️")[0]
		cve_id = cve_id.replace('-', "_")
		cve_id = f"/{cve_id[1:]}"

		desc = textus_splitted[2:-2]
		desc = '\n'.join(desc)
		name   =  textus_splitted[0][7:].split("➡️")[-1]

		return f"♨️\n{textus_splitted[0][6]}\n{cve_id}\n{name}\n{desc}"

	elif textus_splitted[0][0] == "📣":
		print("📣")
		cve_id = textus_splitted[0][4:].split("➡️")[0]
		cve_id = cve_id.replace('-', "_")
		cve_id = f"/{cve_id[1:]}"

		desc = textus_splitted[2:-2]
		desc = '\n'.join(desc)
		name   =  textus_splitted[0][5:].split("➡️")[-1]

		return f"♨️\n{textus_splitted[0][3]}\n{cve_id}\n{name}\n{desc}"

def json_parser(json_object):
	val = json_object["RESULTS_EXPLOIT"]
	text_buffer = []
	file_buffer = []
	#📳🔻🔺🔹✍️🛅❇️

	for u in val[:3]:

		buffer_str = ""
		cve_id = u['Codes'].replace('-', "_")
		cve_id = f"/{cve_id[1:]}"
		buffer_str = f"{cve_id}\n" 

		#buffer_str = f"{buffer_str} \n" 
		buffer_str = f"⚛️Название: {u['Title']}\n" 
		buffer_str = f"{buffer_str}\n🟪EDB-ID: {u['EDB-ID']}"
		buffer_str = f"{buffer_str}\n🔻Опубликован: {u['Date_Published']}"
		buffer_str = f"{buffer_str}\n🔺Добавлен: {u['Date_Added']}"
		buffer_str = f"{buffer_str}\n♦️Обновлен: {u['Date_Updated']}"
		buffer_str = f"{buffer_str}\n🔲Автор: {u['Author']}"
		buffer_str = f"{buffer_str}\n🔲Тип: {u['Type']}"
		buffer_str = f"{buffer_str}\n🟪Платформа: {u['Platform']}"
		if u["Verified"] == "1":
			buffer_str = f"{buffer_str}\nПроверен: ✅\n"
		else:
			buffer_str = f"{buffer_str}\nПроверен: ❌\n"
		buffer_str = f"{buffer_str}----------------------------------\n" 


		file_buffer.append(u["Path"])
		text_buffer.append(buffer_str)
	return text_buffer, file_buffer





def splitter(big_text):
	array_ids = []
	array_text = []
	for u in big_text:
		all_text = u.split('|||')
		cve_id_base = all_text[0]
		#print(cve_id_base)
		cve_id = cve_id_base.replace('-', "_")
		cve_id = cve_id.upper()[1:]
		array_ids.append(f"/{cve_id}")
		array_text.append(f"{cve_id_base}\n{all_text[-1]}")

	return array_text, array_ids


def create_report(info_cve, answ, github_data):

	crit = info_cve[7].split(":")[-1][1:]

	if crit == "N/A":
		crit_emoji = "🟩"
	elif crit == "MEDIUM":
		crit_emoji = "🟨"
	elif crit == "HIGH":
		crit_emoji = "🟧"
	elif crit == "CRITICAL":
		crit_emoji = "🟥"
	else:
		crit_emoji = "❗️"

	links = re.findall(r'\[.*?\]\((.*?)\)', github_data)
	links_Poc = '\n'.join(links[1:])
	description = re.search(r'### Description\n\n(.+?)\n\n', github_data, re.DOTALL)
	reference = re.search(r'#### Reference\n(.+?)\n\n', github_data, re.DOTALL)
	git_link = re.search(r'#### Github\n(.+?)\n\n', github_data, re.DOTALL)
	print(github_data)

	print(info_cve[0][1:])
	searchsploit = search_sploit.search(info_cve[0][1:])

	searchsploit = json.loads(searchsploit)

	searchsploit_text, searchsploit_file = json_parser(searchsploit)

	print(searchsploit_text, searchsploit_file)
	
	if searchsploit_text:
		searchtext = f"Searchsploit:\n{searchsploit_text[0]}"
	else:
		searchtext = ''

	if github_data != "404: Not Found":
		rep = f"""
⚛️{info_cve[0]}
🔗nist - {info_cve[1]}\n🔗mitre - {links[0]}
📎{info_cve[2]}
📌{info_cve[3]}
⛔️{info_cve[4]}
🔺{info_cve[5]}
🔻{info_cve[6]}
{crit_emoji}{info_cve[7]}\n
👁‍🗨{info_cve[8]}\n\n👁‍🗨{description.group(1)}
👁‍{info_cve[9]}

Reference:\n{reference.group(1)}

🤖ChatGPT:
{answ}

Github Poc:
{git_link.group(1)}

{searchtext}
	"""
	else:
		rep = f"""
⚛️{info_cve[0]}
🔗nist - {info_cve[1]}
📎{info_cve[2]}
📌{info_cve[3]}
⛔️{info_cve[4]}
🔺{info_cve[5]}
🔻{info_cve[6]}
{crit_emoji}{info_cve[7]}\n
👁‍🗨{info_cve[8]}
👁‍{info_cve[9]}

Reference:N/A

🤖ChatGPT:
{answ}

{searchtext}

	"""
	if searchsploit_file:
		return rep, searchsploit_file[0]
	else:
		return rep, []

def create_report_short(answ):
	return "\n".join(answ)