import requests
import nvdlib
import datetime
import config



class HabrMentions:

    def get(self, cve):
        req = requests.get("https://habr.com/kek/v2/articles/", params={"query": cve})
        response = req.json()
        return response["searchStatistics"]["articlesCount"]

class MentionService:

    def __init__(self):
        self.habr = HabrMentions()

    def get_all_mentions(self, count, cve):
        return count + self.habr.get(cve)

    def get_mentions(self, service, cve):
        if service == "habr":
            return self.habr.get(cve)
        else:
            raise Exception("Invalid service")



class NistService:

    def __init__(self):
        self.nvdlib = nvdlib

    def search_cve_by_id(self, query, limit):
        return self.nvdlib.searchCVE(cveId=query, key=config.NIST_API_KEY, delay=0.6)

    def search_cve(self, query, limit):
        return self.nvdlib.searchCVE_V2(keywordSearch=query, limit=limit, key=config.NIST_API_KEY)

    def get_last_cve(self, days, limit):
        end = datetime.datetime.now()
        start = end - datetime.timedelta(days=days)
        return self.nvdlib.searchCVE(pubStartDate=start, limit=limit, pubEndDate=end, key=config.NIST_API_KEY)

class CVE:
    def __init__(self, cve_data):
        self.id = cve_data.id
        self.url = cve_data.url
        self.published = cve_data.published
        self.lastModified = cve_data.lastModified
        self.v31score = getattr(cve_data, "v31score", 'N/A')
        self.v31exploitability = getattr(cve_data, "v31exploitability", 'N/A')
        self.v31severity = getattr(cve_data, "v31severity", 'N/A')
        self.cpe = cve_data.cpe[0].criteria.split(":") if hasattr(cve_data, 'cpe') and cve_data.cpe else None
        self.descriptions = cve_data.descriptions


    def returns(self, mention_service):
        return_arr = []
        return_arr.append(f"| {self.id}")
        return_arr.append(f"Ссылка: {self.url}")
        return_arr.append(f"Уязвимая версия продукта: {self.cpe[5] if self.cpe else 'N/A'}")
        return_arr.append(f"Дата публикации: {self.published}")
        return_arr.append(f"Последнее редактирование: {self.lastModified}")
        return_arr.append(f"CVSS SCORE: {self.v31score}")
        return_arr.append(f"EPSS SCORE: {self.v31exploitability}")
        return_arr.append(f"Критичность: {self.v31severity}")
        return_arr.append(f"Описание: {self.descriptions[0].value if self.descriptions else 'N/A'}")
        return_arr.append(f"Упоминания на хабре: {mention_service.get_mentions('habr', self.id)}")
        return return_arr

    def returns_weekly(self, arr, mention_service):
        return_arr = []
        for u in arr:
            return_arr.append(f"⚛️ /{u.id.replace('-', '_')}\n🔗Ссылка:\n{ {u.url}}")
        return return_arr


class CveInfo:
    def __init__(self, current=None):
        self.nist_service = NistService()
        self.mention_service = MentionService()
        #self.last_cve = self.nist_service.get_last_cve(days=7, limit=10)
        #print(self.last_cve)
        #if current == None:
        #    self.cve_objects = [CVE(cve) for cve in self.last_cve]
        #else:
        #    self.cve_objects = CVE(current)

    def print_info(self):
        for cve in self.cve_objects:
            cve.prints(self.mention_service)
        return self.mention_service

    def print_by_id(self, ids):
        try:
            current = self.nist_service.search_cve_by_id(ids, limit=1)
            cve_objects = CVE(current[0])
            cve_objects = cve_objects.returns(self.mention_service)
            return cve_objects, current[0]
        except Exception as e:
            return "Мы не можем найти такую уязвимость, проверьте написание", None


    def print_by_keyword(self, keyword):
        try:
            current = self.nist_service.search_cve(keyword, limit=10)
            cve_objects_arr = []
            for u in current:
                cve_objects = CVE(current)
                print(cve_objects)
                cve_objects = cve_objects.returns(self.mention_service)
                cve_objects_arr.append(cve_objects)

            return cve_objects_arr
        except Exception as e:
            return "Мы не можем найти такую уязвимость, проверьте написание", None

    #def print_weekly(self):
    #    self.last_cve = self.nist_service.get_last_cve(days=7, limit=10)
    #    cve_objects = [CVE(cve) for cve in self.last_cve]
    #    cve_objects = self.returns_weekly(self.mention_service)

    def print_daily(self):
        last_cve = self.nist_service.get_last_cve(days=1, limit=10)
        return CVE.returns_weekly(self, [CVE(cve) for cve in last_cve], self.mention_service)

    def print_weekly(self):
        last_cve = self.nist_service.get_last_cve(days=7, limit=10)
        return CVE.returns_weekly(self, [CVE(cve) for cve in last_cve], self.mention_service)

