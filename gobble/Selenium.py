from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
import csv
import time

from stockapi.models import (
    KospiNet,
    KosdaqNet,
    ETFNet,
)

class Shinhan_selenium(object):

    def __init__(self):
        self.browser = webdriver.Chrome('./chromedriver')
        self.browser = webdriver.PhantomJS('./phantomjs/bin/phantomjs')
        self.today_date = datetime.today().strftime('%Y%m%d')
        self.market_net = {'KOSPI':KospiNet, 'KOSDAQ':KosdaqNet, 'ETF':ETFNet}
        print('webdriver is ready')

    def url_setings(self, urls):
        if urls == 'shinhan':
            self.url = 'http://open.shinhaninvest.com/goodicyber/mk/1206.jsp?code='
        else:
            pass
        return self.url

    def add_log(self, strings):
        path = './gobble/backup/log/log.txt'
        f = open(path, 'a', encoding='utf-8', newline='')
        f.write(strings)
        f.close()

    def get_source(self, url, code):
        self.browser.get(url.format(code))
        self.html = self.browser.page_source
        return self.html

    def html_parser(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')
        return self.soup

    def soup_findall(self, soup, tags, class_dict=None):
        self.source = soup.findAll(tags, class_dict)
        return self.source

    def scrape_shinhan_buysell(self, tickers):
        success = False
        csv_list = []
        data_list = []
        A = time.time()
        for ticker in tickers:
            url = self.url_setings('shinhan')
            html = self.get_source(url, ticker.code)
            soup = self.html_parser(html)
            table = self.soup_findall(soup, 'table', {'class':'content1'})
            tr = self.soup_findall(table[0], 'tr')
            code = ticker
            market = ticker.market_type
            for i in range(2,len(tr)):
                t = tr[i].text.split('\n')
                date = t[1].replace('/','')
                individual = int(t[2].replace(',',''))
                foreign_retail = int(t[3].replace(',',''))
                institution = int(t[4].replace(',',''))
                financial = int(t[5].replace(',',''))
                trust = int(t[6].replace(',',''))
                bank = int(t[7].replace(',',''))
                etc_finance = int(t[8].replace(',',''))
                insurance = int(t[9].replace(',',''))
                pension = int(t[10].replace(',',''))
                etc_corporate = int(t[11].replace(',',''))
                net_inst = self.market_net[market](date=date,
                                                  code=code,
                                                  individual=individual,
                                                  foreign_retail=foreign_retail,
                                                  institution=institution,
                                                  financial=financial,
                                                  trust=trust,
                                                  bank=bank,
                                                  etc_finance=etc_finance,
                                                  insurance=insurance,
                                                  pension=pension,
                                                  etc_corporate=etc_corporate,)
                data_list.append(net_inst)
        self.market_net[market].objects.bulk_create(data_list)
        B = time.time()
        success = True
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        strings = "The number of data : {}, Time :{}, lap-time{}".format(len(data_list), now, B-A)
        self.add_log(strings)
        return success, "Data request complete {} sec".format(B-A)
