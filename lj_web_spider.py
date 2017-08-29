# -*- coding: utf-8 -*-
__author__ = 'liaoben'

import requests
from bs4 import BeautifulSoup
import xlsxwriter
from datetime import datetime
from lj_db import Db
from lj_models import *
from lj_charts import Charts

class LjSpider:

    def __init__(self,crawl_page=10,region='donghugaoxin',price='p4',room='l3',
                 order='co32l3p4',url='https://wh.lianjia.com/ershoufang',*args):
        self.region = region
        self.price = price
        self.room = room
        self.order = order
        self.crwal_page = crawl_page
        self.folder = 'g:/ljdata/'
        self.db = Db()
        self.url= url
        map_list = [self.region,self.price,self.order]
        map_list.extend(args)
        map(self.url_generate,map_list)
        self.url +='/pg%s/'
        self.result = []
        self.count = 0
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept':'text/html;q=0.9,*/*;q=0.8',
            'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding':'gzip',
            'Connection':'close',
         }

    def url_generate(self,content):
        if content:
            self.url = self.url+'/'+content

    def crwal(self,url):
        html = requests.get(url,allow_redirects = False,headers = self.headers).content
        return self.content_handler(html)

    def content_handler(self,html):
        lj=BeautifulSoup(html,'html.parser')
        house_info = lj.find_all('li',attrs={'class':'clear'})
        print len(house_info)
        result = []
        for house in house_info:
            base_info = house.find_all('div',attrs={'class':'houseInfo'})[0].text
            xiaoqu_name,room_type,room_size,room_way = base_info.split('|')[:4]
            # xiaoqu_name = base_info.find_all('a')[0].text
            total = house.find_all('div',attrs={'class':'totalPrice'})[0].text.replace(u'万','')
            unit = house.find_all('div',attrs={'class':'unitPrice'})[0].get('data-price')
            mask = house.find_all('div',attrs={'class':'title'})[0].find_all('a')[0].get('href')
            tags = house.find_all('div',attrs={'class':'tag'})[0].text
            for tag in house.find_all('div',attrs={'class':'tag_box'}):
                tags = tags + tag.text + ','
            tags = tags.replace('\n','')
            tags = tags[:-1]
            ret = [mask,xiaoqu_name,room_type,room_size,room_way,total,unit,tags]
            ret = [x.strip() for x in ret]
            # self.result.append(ret)
            result.append(ret)
        return result

    def start(self,save='excel'):
        for i in range(self.crwal_page):
            url = self.url % (str(i+1))
            print 'start cwal url:',url
            ret = self.crwal(url)
            for r in ret:
                self.result.append(r)
            print len(self.result)
        if save == 'excel':
            self.write_to_excel(self.result)
        elif save == 'db':
            self.write_to_sql(self.result)
        elif save == 'chart':
            self.draw()

    def write_to_excel(self,data):
        import os
        if not os.path.exists(self.folder):
            os.mkdir(self.folder)
        fname = self.folder+self.region + datetime.now().strftime( '%Y%m%d%H%M%S')+'.xlsx'
        wb = xlsxwriter.Workbook(fname)
        ws = wb.add_worksheet()
        data = [x for x in data if not isinstance(x,type(None))]
        unit_size = len(data[0])
        ws.set_column(0,unit_size,22)
        for i in range(len(data)):
            for j in range(unit_size):
                content = self.ensure_writeble(data[i][j])
                ws.write(i+1,j,content)
        wb.close()

    def write_to_sql(self,data):
        for d in data:
            temp_list = ['mask','village','type','size','position','total','unit','tags']
            temp_dict = {}
            for i in range(len(d)):
                temp_dict[temp_list[i]] = d[i]
            house_web_info = InformationWeb(**temp_dict)
            self.db.merge(house_web_info)
            self.count+=1
            self.db.commit()
        print self.count

    def ensure_writeble(self,content):
        try:
            content = content.decode('utf-8')
        except:
            pass
        return content

    def draw(self):
        chart = Charts(['Nov', 'Dec', 'Jan', 'Feb'], [2, 10, 4, 5])
        chart.draw()

if __name__ == '__main__':
    LjSpider(60,price='',order='').start('db')