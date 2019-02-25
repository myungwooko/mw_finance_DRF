from django.db import migrations
from bs4 import BeautifulSoup
import requests
# from django.apps import apps

def menu_set(apps, schema_editor):
    page_url = 'https://finance.naver.com/marketindex/worldExchangeList.nhn?key=exchange&page='
    pages = []
    count = 1
    Currency = apps.get_model('mw_finance', 'Currency')
    while True:
        one = page_url + str(count)
        if count != 1:
            if requests.get(one).text != requests.get(pages[len(pages) - 1]).text:
                pages.append(one)
                count += 1
            else:
                break
        else:
            pages.append(one)
            count += 1

    currency_names = []
    for page in pages:
        html = requests.get(page).text
        soup = BeautifulSoup(html, 'html.parser')
        for line in soup.select('tr'):
            title = line.select('.tit')
            if len(title) != 0:
                currency_names.append(title[0].text)


    currency = Currency(name="** 전체 **")
    currency.save()

    for currency_name in currency_names:
        currency = Currency(name=currency_name)
        currency.save()

class Migration(migrations.Migration):

    dependencies = [
        ('mw_finance', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(menu_set),
    ]