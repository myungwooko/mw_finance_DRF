from .models import Currency, Currency_info
from django.forms.models import model_to_dict
from datetime import datetime, date
from bs4 import BeautifulSoup
from operator import itemgetter
import requests
from .serializers import CurrencyInfoSerializer



today = date.today()



class Methods:

    def __init__(self):
        pass

    @staticmethod
    def page(url):
        pages = []
        count = 1
        while True:
            one = url + str(count)
            current_page = requests.get(one).text
            if count != 1:
                if current_page != pages[len(pages) - 1]:
                    pages.append(current_page)
                    count += 1
                else:
                    break
            else:
                pages.append(current_page)
                count += 1
        return pages




    @staticmethod
    def instance_to_dict(i):
        dict = {}
        i = model_to_dict(i)
        keys = list(i.keys())
        for key in keys:
            dict[key] = i[key]
        return dict




    @staticmethod
    def currency_name_by_id(id):
        currency = Currency.objects.all().filter(id=id)[0]
        name = currency.name
        return name




    @staticmethod
    def currency_id_by_name(name):
        currency_id = Currency.objects.all().filter(name=name)[0]
        return currency_id.id




    @classmethod
    def insert_currency_info(cls, trimmed_list):
        list = trimmed_list
        currency_id = cls.currency_id_by_name(list[0])

        #com_bef <= comparing_before <= 전일대비
        com_bef = list[3].split(' ')
        last_idx1 = len(com_bef) - 1
        com_bef = com_bef[last_idx1]
        currency_info = Currency_info.objects.all().filter(currency_id=currency_id).filter(created_at__gte=today)

        if not currency_info.exists():
            if len(list[3:]) == 2:
                info = Currency_info(name=list[0], symbol=list[1], current_price=float(''.join(list[2].split(','))), comparing_yesterday=float(com_bef), change=0.00, currency_id=Currency.objects.filter(id=currency_id)[0], created_at= datetime.now())
                info.save()
            else:
                plus_minus = list[4][len(list[4])-1]
                if plus_minus == '+':
                    plus_minus_operator = 1
                else:
                    plus_minus_operator = -1
                info = Currency_info(name=list[0], symbol=list[1], current_price=float(''.join(list[2].split(','))), comparing_yesterday=plus_minus_operator * float(com_bef),
                                    change=plus_minus_operator * float(('0.'+ list[len(list)-1].split('.')[1])[0:-1]), currency_id=Currency.objects.filter(id=currency_id)[0], created_at= datetime.now())
                info.save()




    @classmethod
    def find_and_insert(cls, currency_id, pages):
        name = cls.currency_name_by_id(currency_id)
        html_line = cls.html_line_by_name(name, pages)
        trimmed_list = cls.trimming(html_line)
        cls.insert_currency_info(trimmed_list)




    @staticmethod
    def html_line_by_name(name, pages):
        for html in pages:
            soup = BeautifulSoup(html, 'html.parser')
            for html_line in soup.select('tr'):
                title = html_line.select('.tit')
                if len(title) != 0:
                    title = title[0].text
                    if name == title:
                        return html_line




    @staticmethod
    def trimming(html_line):
        trimmed_list = []
        rough = html_line.text.split('\n')
        for ele in rough:
            if len(ele) != 0 and ele != '\t\t\t\t\t\t\t' and ele != '\t\t\t\t\t\t':
                trimmed_list.append(ele)
        return trimmed_list




    @classmethod
    def currency_id_none_and_len_num(cls, currency_infos, pages):
        all_id_list = list(range(2, 117))
        today_id_list = currency_infos.values_list('currency_id', flat=True)
        not_today_ids = (set(all_id_list) - set(today_id_list))
        result = []
        for id in not_today_ids:
            cls.find_and_insert(id, pages)
        currency_infos = Currency_info.objects.filter(created_at__gte=today)
        serializer = CurrencyInfoSerializer(currency_infos, many=True)
        result = sorted(serializer.data, key=itemgetter('currency_id'))
        return result




    @classmethod
    def currency_id_none_and_len_zero(cls, pages):
        result = []
        for html in pages:
            soup = BeautifulSoup(html, 'html.parser')
            count = 0
            for line in soup.select('tr'):
                if count == 0:
                    count += 1
                    pass
                else:
                    trimmed_list = cls.trimming(line)
                    cls.insert_currency_info(trimmed_list)
        currency_infos = Currency_info.objects.filter(created_at__gte=today)
        serializer = CurrencyInfoSerializer(currency_infos, many=True)
        return serializer.data




    @classmethod
    def currency_id_not_1(cls, currency_id, pages):
        currency_id_object = Currency(id=currency_id)
        currency_info = Currency_info.objects.filter(created_at__gte=today).filter(currency_id=currency_id_object)
        if currency_info.exists():
            serializer = CurrencyInfoSerializer(currency_info[0])
            return serializer.data
        else:
            cls.find_and_insert(currency_id, pages)
            currency_info = Currency_info.objects.filter(created_at__gte=today).filter(currency_id=currency_id_object)
            serializer = CurrencyInfoSerializer(currency_info[0])
            return serializer.data
