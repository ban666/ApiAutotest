# -*- coding: utf-8 -*-
__author__ = 'liaoben'

import requests
from bs4 import BeautifulSoup
import xlsxwriter
from datetime import datetime
from lj_db import Db
from lj_models import *

class LjSpider:

    def __init__(self,crawl_page=10,region='donghugaoxin',price='p4',room='l3',
                 order='co32l3p4',url='https://m.lianjia.com/wh/ershoufang',*args):
        self.region = region
        self.price = price
        self.room = room
        self.order = order
        self.crwal_page = crawl_page
        self.folder = 'g:/ljdata/'
        self.db = Db()
        # self.url='https://m.lianjia.com/wh/ershoufang/%s/%s/%s/%s/pg%s/'
        self.url='https://m.lianjia.com/wh/ershoufang'
        map_list = [self.region,self.price,self.order]
        map_list.extend(args)
        map(self.url_generate,map_list)
        self.url +='/pg%s/'
        self.result = []

    def url_generate(self,content):
        if content:
            self.url = self.url+'/'+content

    def crwal(self,url):
        html = requests.get(url,allow_redirects = False).content
        return self.content_handler(html)

    def content_handler(self,html):
        lj=BeautifulSoup(html,'html.parser')
        house_info = lj.find_all('li',attrs={'class':'pictext'})
        result = []
        for house in house_info:
            base_info = house.find_all('div',attrs={'class':'item_other text_cut'})[0].text
            room_type,room_size,room_way,xiaoqu_name = base_info.split('/')
            total = house.find_all('span',attrs={'class':'price_total'})[0].text.strip(u'万')
            unit = house.find_all('span',attrs={'class':'unit_price'})[0].text.strip(u'元/平')
            mask = house.find_all('a',attrs={'class':'a_mask'})[0].get('href')
            tags = ''
            for tag in house.find_all('div',attrs={'class':'tag_box'}):
                tags = tags + tag.text + ','
            tags = tags.replace('\n','')
            tags = tags[:-1]
            ret = [mask,xiaoqu_name,room_type,room_size,room_way,total,unit,tags]
            for r in ret:
                print r
            # self.result.append(ret)
            result.append(ret)
        return result

    def start(self,save='excel'):
        for i in range(self.crwal_page):
            url = self.url % (str(i+1))
            ret = self.crwal(url)
            for r in ret:
                self.result.append(r)
        if save == 'excel':
            self.write_to_excel(self.result)
        elif save == 'db':
            self.write_to_sql(self.result)

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
            house = Information(**temp_dict)
            self.db.merge(house)
            self.db.commit()

    def ensure_writeble(self,content):
        try:
            content = content.decode('utf-8')
        except:
            pass
        return content

if __name__ == '__main__':
    LjSpider(1,price='').start('db')