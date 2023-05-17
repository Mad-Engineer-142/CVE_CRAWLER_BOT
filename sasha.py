import nvdlib
import datetime
import pycvesearch
import matplotlib.pyplot as plt

#
"""print("Выберите промежуток времени для вывода CVE:\n1. День\n2. Неделя\n3. Месяц\n4. Свой промежуток")

end = datetime.datetime.now()
if a == '1':
  start = end - datetime.timedelta(days=1)
elif a == '2':
  start = end - datetime.timedelta(days=7)
elif a == '3':
  start = end - datetime.timedelta(days=30)
elif a == '4':
  a1 = input("Введите начальный период в формате (YYYY-MM-DD): ")
  a2 = input("Введите конечный период в формате (YYYY-MM-DD): ")
  a1 += " 00:00"
  a2 += " 00:00"
  start = a1
  end = a2
else:
  print("Нет такого варианта ответа.")


r = nvdlib.searchCVE(pubStartDate=start, pubEndDate=end, key='3528d822-f54a-4929-92c1-417c79645a5d', delay=0.6)
"""
def get_cve(start, end):
  r = nvdlib.searchCVE(pubStartDate=start, pubEndDate=end, key='3528d822-f54a-4929-92c1-417c79645a5d', delay=0.6)
  buffer_cve = []
  for i in range(len(r)):
    cve = r[i]
    buffer_string = ""
    buffer_string = f"{buffer_string}\n{cve.id}|||"
    print("CVE ID:", cve.id)
    buffer_string = f"{buffer_string}\nСсылка на источник: {cve.url}"
    print("Ссылка на источник:", cve.url)

    if hasattr(cve, 'v31score'):
      buffer_string = f"{buffer_string}\nCVSS 3.1 Score: {cve.v31score}"
      print("CVSS 3.1 Score:", cve.v31score)
    else:
      buffer_string = f"{buffer_string}\nCVSS 3.1 Score: N/A"
      print("CVSS 3.1 Score: N/A")

    if hasattr(cve, "v31severity"):
      buffer_string = f"{buffer_string}\nУровень критичности: {cve.v31severity}"
      print("Уровень критичности:", cve.v31severity)
    else:
      buffer_string = f"{buffer_string}\nУровень критичности: N/A"
      print("Уровень критичности: N/A")
      buffer_string = f"{buffer_string}\nМетрики {cve.metrics}"
      print("Метрики:", cve.metrics)

    if hasattr(cve, "v31exploitability"):
      buffer_string = f"{buffer_string}\nEPSS рейтинг: {cve.v31exploitability}\n"
      print("EPSS рейтинг:", cve.v31exploitability)
    else:
      buffer_string = f"{buffer_string}\nEPSS рейтинг: N/A"
      print("EPSS рейтинг: N/A")

    pub = cve.published
    pub = pub[:10] + ' ' + pub[11:-4]
    print("Дата/время регистрации CVE:", pub)
    buffer_string = f"{buffer_string}\nДата/время регистрации CVE: {pub}\n"
    print("\n\n")
    buffer_cve.append(buffer_string)
  return buffer_cve

#get_cve(start, end)