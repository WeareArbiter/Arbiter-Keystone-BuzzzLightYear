from selenium import webdriver
from bs4 import BeautifulSoup
import csv

browser = webdriver.Chrome('./chromedriver')
browser = webdriver.PhantomJS('./phantomjs/bin/phantomjs')
# browser.implicitly_wait(3)
browser.get('http://open.shinhaninvest.com/goodicyber/mk/1206.jsp?code=005930')
f = open('./gobble/backup_csv/kospi/buysell/005930.csv', 'w', encoding='utf-8', newline='')
fieldnames = ['date','individual','foreign_retail','institution','finance',
              'etc_finance','trust','bank', 'insurance','pension','etc_corporate']
hd = csv.DictWriter(f,fieldnames=fieldnames)
hd.writeheader()
f.close()

csv_list = []
html = browser.page_source
soup = BeautifulSoup(html, 'html.parser')
table = soup.findAll('table', {'class':'content1'})
tr = table[0].findAll('tr')
tr[3].text.split('\n')
code = '005930'
for i in range(2,len(tr)):
    t = tr[i].text.split('\n')
    date = t[1].replace('/','')
    individual = int(t[2].replace(',',''))
    foreign_retail = int(t[3].replace(',',''))
    institution = int(t[4].replace(',',''))
    finance = int(t[5].replace(',',''))
    trust = int(t[6].replace(',',''))
    bank = t[7].replace(',','')
    etc_finance = t[8].replace(',','')
    insurance = t[9].replace(',','')
    pension = t[10].replace(',','')
    etc_corporate = t[11].replace(',','')
    # ticker_inst = market_net[market](date=date,
    #                                  code=code,
    #                                  individual=individual,
    #                                  foreign_retail=foreign_retail,
    #                                  institution=institution,
    #                                  finance=finance,
    #                                  trust=trust,
    #                                  bank=bank,
    #                                  etc_finance=etc_finance,
    #                                  insurance=insurance,
    #                                  pension=pension,
    #                                  etc_corporate=etc_corporate,)
    # data_list.append(ticker_inst)
    row_list = [date,individual,foreign_retail,institution,finance,etc_finance,trust,bank,
                insurance,pension,etc_corporate]
    csv_list.append(row_list)
    f = open('./gobble/backup_csv/kospi/buysell/005930.csv', 'a', encoding='utf-8', newline='')
    wr = csv.writer(f)
    wr.writerows(csv_list)
    f.close()
